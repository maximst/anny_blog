from django.db import models
from django.contrib.auth.models import User

from tag.models import ArticleTaggedItem, TaggableManagerN


class Blog(models.Model):
    title = models.CharField(max_length=128, unique=True)
    preview = models.TextField(default='', blank=True)
    body = models.TextField(default='')
    slug = models.SlugField(max_length=128, unique=True)
    deleted = models.BooleanField(default=False)
    author = models.ForeignKey(User, null=True)
    front_page = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    tags = TaggableManagerN(through=ArticleTaggedItem)

    def __unicode__(self):
        return u'%s' % self.title
