from bambu_attachments.helpers import upload_attachment_file
from bambu_attachments.models import Attachment
from bambu_blog import helpers, excerpt
from bambu_blog.querysets import *
from django.conf import settings
from django.contrib.contenttypes import fields as generic
from django.db import models, transaction
from django.template import Template, Context
from django.utils.timezone import now
from hashlib import md5
from mimetypes import guess_type
from taggit.managers import TaggableManager

if 'bambu_webhooks' in settings.INSTALLED_APPS:
    from bambu_webhooks import site, send

COMMENTS_MODEL = getattr(settings, 'BLOG_COMMENTS_MODEL', 'bambu_comments.Comment')

class Category(models.Model):
    """A category under which blog posts can be filed"""

    name = models.CharField(max_length = 100, db_index = True)
    """The category name"""

    slug = models.SlugField(max_length = 100, unique = True)
    """The category slug (unique)"""

    def __unicode__(self):
        return self.name

    @property
    def post_percent(self):
        """The percentage of total blog posts that are in this category"""
        count = float(getattr(self, 'post_count', self.posts.live().count()))
        all_count = float(Post.objects.live().count())

        return count / all_count * 100.0

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'
        db_table = 'blog_category'
        app_label = 'bambu_blog'

class PostQuerySet(models.QuerySet):
    """
    A custom queryset that adds a few utility functions to the standard one
    """

    def live(self):
        """Returns only posts in the future that are marked as published"""
        return self.filter(
            date__lte = now(),
            published = True
        )

    def css(self, rendered = False):
        """Returns rendered CSS for all of the posts in the query"""
        if rendered:
            return '\n\n'.join(
                [
                    (post.render_css() or u'') for post in self.all()
                ]
            )
        else:
            return '\n\n'.join(
                [
                    (css or u'') for css in self.values_list('css', flat = True)
                ]
            )

    def with_featured_attachments(self, only = False):
        queryset = self.extra(
            select = {
                'featured_attachment_file': 'SELECT file FROM attachments_attachment AS a ' \
                'INNER JOIN django_content_type AS t ON t.id = a.content_type_id ' \
                'WHERE t.app_label = \'bambu_blog\' AND t.model = \'post\' ' \
                'AND a.object_id = blog_post.id AND a.featured'
            }
        )

        if only:
            queryset = queryset.filter(
                attachments__featured = True
            ).distinct('date', 'pk')

        return queryset

    def with_comment_counts(self):
        return self.extra(
            select = {
                'comment_count': 'SELECT COUNT(*) FROM comments_comment AS c ' \
                'INNER JOIN django_content_type AS t ON t.id = c.content_type_id ' \
                'WHERE t.app_label = \'bambu_blog\' AND t.model = \'post\' ' \
                'AND c.object_id = blog_post.id AND c.approved'
            }
        )

class Post(models.Model):
    """
    A blog post
    """

    author = models.ForeignKey('auth.User', related_name = 'blog_posts')
    """The ``auth.User`` that wrote the post"""

    title = models.CharField(max_length = 100, null = True, blank = True)
    """The title of the post (optional)"""

    slug = models.SlugField(max_length = 100, db_index = True)
    """The slug of the post (if no title is given, a slug is generated from the total count of blog
    posts"""

    date = models.DateTimeField(db_index = True)
    """The post date"""

    published = models.BooleanField(default = True)
    """Whether the post is published (``True`` by default)"""

    broadcast = models.BooleanField(default = False, editable = False)
    """Whether a webhook event was fired when the post was published"""

    body = models.TextField()
    """The body of the post. By default this is a plain text field within the admin, but you can install
    django-markitup or django-tinymce and the admin will automatically detect one of those apps.
    Regardless of textbox interface, the body is always run through PyQuery's HTML parser, in order to
    generate a viable, readable excerpt that ignores references to things like oEmbed resources and
    images, and flattens lists, headings, quotes etc"""

    excerpt = models.TextField(null = True, blank = True, editable = False)
    """A short, automatically-generated excerpt for the post"""

    css = models.TextField(null = True, blank = True)
    """Custom CSS for the post (great for making custom-designed pages for each post)"""

    tags = TaggableManager()
    """The tags assigned to the post (optional)"""

    categories = models.ManyToManyField(Category, related_name = 'posts', blank = True)
    """The categories assigned to the post (optional)"""

    attachments = generic.GenericRelation(Attachment)
    """The attachments (images and other media) attached to the post (optional)"""

    comments = generic.GenericRelation(COMMENTS_MODEL)
    """A generic link to a comment model, as defined in the ``BLOG_COMMENTS_MODEL`` setting"""

    objects = PostQuerySet.as_manager()

    @models.permalink
    def get_absolute_url(self):
        return (
            'blog_post', (
                str(self.date.year).zfill(4),
                str(self.date.month).zfill(2),
                str(self.date.day).zfill(2),
                self.slug
            )
        )

    def __unicode__(self):
        return self.title or u'(Untitled)'

    def next_post(self):
        """Returns the next blog post in the sequence (irrespective of category, tag or author)"""
        try:
            return Post.objects.live().filter(date__gt = self.date)[0]
        except:
            pass

    def previous_post(self):
        """Returns the previous blog post in the sequence (irrespective of category, tag or author)"""
        try:
            return Post.objects.live().filter(date__lt = self.date).latest()
        except:
            pass

    def render_css(self):
        """
        Runs CSS through Django's templating engine, allowing you to write CSS that references
        attachment URLs and the post ID without actually having to know that they are
        """

        template = Template(self.css)
        context = Context(
            {
                'attachments': self.attachments.all(),
                'slug': self.slug,
                'pk': self.pk,
                'id': self.pk
            }
        )

        return template.render(context)

    def featured_attachment(self):
        """Returns the first attachment for the post, that's marked as Featured"""
        if hasattr(self, 'featured_attachment_file'):
            return self.featured_attachment_file

        try:
            return self.attachments.filter(featured = True)[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        publish = False
        if self.pk:
            old = Post.objects.get(pk = self.pk)
            if self.published and not old.published:
                publish = True
        elif self.published:
            publish = True

        if not self.slug and not self.title:
            slug = str(
                Post.objects.filter(
                    date__year = self.date.year,
                    date__month = self.date.month,
                    date__day = self.date.day
                ).count() + 1
            )

            while Post.objects.filter(
                date__year = self.date.year,
                date__month = self.date.month,
                date__day = self.date.day,
                slug = slug
            ).exists():
                slug = str(int(slug) + 1)

            self.slug = slug

        if self.body:
            self.excerpt = excerpt(self.body)

        super(Post, self).save(*args, **kwargs)
        if publish and self.date <= now():
            self.publish()

    def publish(self):
        if 'bambu_webhooks' in settings.INSTALLED_APPS:
            send('post_published', self.author,
                {
                    'id': self.pk,
                    'title': self.title,
                    'slug': self.slug,
                    'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'body': self.body,
                    'tags': [t for t in self.tags.values_list('slug', flat = True)],
                    'categories': [c for c in self.categories.values_list('slug', flat = True)],
                    'attachments': [
                        a.file.url for a in self.attachments.all()
                    ]
                },
                md5('blogpost:%d' % self.pk).hexdigest()
            )

        self.broadcast = True

    class Meta:
        ordering = ('-date',)
        get_latest_by = 'date'
        db_table = 'blog_post'
        app_label = 'bambu_blog'

class PostUpload(models.Model):
    """
    A temporary holding place for media uploaded via XML-RPC
    """

    file = models.FileField(max_length = 255, upload_to = upload_attachment_file)
    url = models.CharField(max_length = 255, db_index = True)
    size = models.PositiveIntegerField(editable = False)
    mimetype = models.CharField(max_length = 50, editable = False, db_index = True)

    def __unicode__(self):
        return self.title

    def convert_to_attachment(self, post):
        """Converts the temporary uploaded file into an attachment"""
        with transaction.atomic():
            attachment = post.attachments.create(
                file = self.file,
                size = self.size,
                mimetype = self.file.size
            )

            self.delete()

        return attachment

    def save(self, *args, **kwargs):
        if self.file and not self.mimetype:
            self.mimetype, encoding = guess_type(self.file.name)

        if not self.size:
            self.size = self.file.size

        self.url = self.file.url
        super(PostUpload, self).save(*args, **kwargs)

    class Meta:
        db_table = 'blog_post_upload'
        app_label = 'bambu_blog'

if 'bambu_webhooks' in settings.INSTALLED_APPS:
    site.register('post_published',
        description = 'Fired when a post is published',
        staff_only = True
    )
