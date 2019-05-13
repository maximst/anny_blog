from django.contrib.sitemaps import Sitemap
from blog.models import (
    Blog, Comment, BlogImage, InstagramBlog, InstagramImage, Article
)
from tag.models import ArticleTag


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Blog.objects.filter(deleted=False).order_by('id')

    def lastmod(self, obj):
        return obj.create_time

    def location(self, obj):
        return obj.get_url()


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
        return BlogImage.objects.filter().exclude(image='').order_by('id')

    def location(self, obj):
        return obj.image.url


class ArticleTagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ArticleTag.objects.all().order_by('id')

    def location(self, obj):
        return "/tag/%s/" % obj.slug


class InstagramBlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return InstagramBlog.objects.filter(deleted=False, category__enabled=True).order_by('id')

    def location(self, obj):
        return obj.get_url()


class InstagramImageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return InstagramImage.objects.filter().exclude(image='').order_by('id')

    def location(self, obj):
        return obj.image.url


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Article.objects.filter(deleted=False).order_by('id')

    def location(self, obj):
        return obj.get_url()
