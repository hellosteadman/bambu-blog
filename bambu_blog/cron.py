from bambu_cron import CronJob, MINUTE, site
from bambu_blog.models import Post
from django.utils.timezone import now

class PostJob(CronJob):
    frequency = MINUTE
    
    def run(self, logger):
        date = now()
        
        for post in Post.objects.filter(date__lte = date, broadcast = False):
            post.publish()
            post.save()

site.register(PostJob)