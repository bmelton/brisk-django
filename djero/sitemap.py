from django.contrib import sitemaps
import datetime
from djero.models import Topic

# TODO
# This sucks, really.  But I'm not sure if I want to 
# generate the sitemap based on popularity, or if I
# want to limit these results, or what.
class DjeroSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority   = 0.5

    def items(self):
        return Topic.objects.all()    

    def lastmod(self, obj):
        return obj.created
