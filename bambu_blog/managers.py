from django.db.models import Manager

class PostManager(Manager):
    """A custom manager for the ``bambu_blog.Post`` model"""

    def get_query_set(self):
        return self.model.QuerySet(self.model)

    def live(self):
        return self.get_query_set().live()

    def css(self, rendered = False):
        return self.get_query_set().css(rendered)

    def with_featured_attachments(self, only = False):
        return self.get_query_set().with_featured_attachments(only)

    def with_comment_counts(self):
        return self.get_query_set().with_comment_counts()
