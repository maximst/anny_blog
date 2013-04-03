from django.contrib.sitemaps import Sitemap
from blog.models import Blog


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Blog.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.create_time

    def location(self, obj):
        return "/blog/%s/" % obj.slug
