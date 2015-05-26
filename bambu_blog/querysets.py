from django.db import models
from django.utils.timezone import now

class PostQuerySet(models.query.QuerySet):
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
