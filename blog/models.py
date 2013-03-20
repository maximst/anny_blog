from django.db import models
from django.contrib.auth.models import User

from tag.models import ArticleTaggedItem, TaggableManagerN


class Blog(models.Model):
    title = models.CharField(max_length=128, unique=True)
    preview = models.TextField(default='', blank=True)
    body = models.TextField(default='')
    slug = models.SlugField(max_length=128, unique=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True)
    front_page = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    tags = TaggableManagerN(through=ArticleTaggedItem)

    def __unicode__(self):
        return u'%s' % self.title


class Comment(models.Model):
    title = models.CharField(max_length=64, blank=True, default='')
    body = models.TextField()
    user = models.ForeignKey(User, null=True)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    blog = models.ForeignKey(Blog)

    def __unicode__(self):
        return u'%s: %s - %s' % (self.user, self.blog, self.body[:32])


class BlogImage(models.Model):
    title = models.CharField(max_length=128, default='', blank=True)
    blog = models.ForeignKey(Blog)
    image = models.ImageField(upload_to='images')


Blog.num_comments = property(lambda b: Comment.objects.filter(blog=b).count())
Blog.images = property(lambda b: BlogImage.objects.filter(blog=b))
