from django.contrib.sitemaps import Sitemap
from blog.models import Blog, Comment, BlogImage
from tag.models import ArticleTag


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Blog.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.create_time

    def location(self, obj):
        return "/blog/%s/" % obj.slug


class CommentSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Comment.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.create_time

    def location(self, obj):
        return "/blog/%s/#comment-%s" % (obj.blog.slug, obj.id)


class BlogImageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return BlogImage.objects.all().order_by('id')

    def location(self, obj):
        return "%s" % obj.image.url


class ArticleTagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ArticleTag.objects.all().order_by('id')

    def location(self, obj):
        return "/tag/%s/" % obj.slug
