#-*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField

from tag.models import ArticleTaggedItem, TaggableManagerN
from poll.models import Poll

from urlparse import urlparse, parse_qs
import requests
import urllib
import os


class Blog(models.Model):
    IMAGE_ROWS_CHOICES = [(i, i.__str__()) for i in range(1, 11)]
    IMAGE_SIZE = {
        1: 1024,
        2: 500,
        3: 300,
        4: 220,
        5: 170,
        6: 140,
        7: 120,
        8: 100,
        9: 90,
        10: 80,
    }

    title = models.CharField(max_length=128, unique=True)
    preview = models.TextField(default='', blank=True)
    body = models.TextField(default='')
    slug = models.SlugField(max_length=128, unique=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, default=1)
    front_page = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    tags = TaggableManagerN(through=ArticleTaggedItem)
    image_rows = models.PositiveIntegerField(max_length=2, default=1,
                               choices=IMAGE_ROWS_CHOICES)
    video = models.URLField(default='', blank=True)
    poll = models.ForeignKey(Poll, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title

    def image_size(self):
        return '%ix%i' % (self.IMAGE_SIZE[self.image_rows],
                          self.IMAGE_SIZE[self.image_rows])

    def image_width(self):
        return self.IMAGE_SIZE[self.image_rows]

    def image_size_precent(self):
        IMAGE_SIZE = {
            1: 90,
            2: 45,
            3: 30,
            4: 22,
            5: 18,
            6: 15,
            7: 12,
            8: 11,
            9: 10,
            10: 9,
        }
        return IMAGE_SIZE[self.image_rows].__str__()

    def embed_video(self):
        url = urlparse(self.video)
        if 'youtube' in url.netloc:
            query = parse_qs(url.query)
            return ('<iframe width="400" height="300" '
                    'src="%s://%s/embed/%s'
                    '?feature=player_detailpage&wmode=transparent" '
                    'frameborder="0" '
                    'allowfullscreen></iframe>') % (url.scheme, url.netloc,
                                                              query['v'][0])
        elif 'vimeo' in url.netloc:
            digits = map(str, range(10))
            video_id = ''.join(filter(lambda i: i in digits, list(url.path)))
            return ('<iframe src="%s://player.vimeo.com/video/%s?wmode=transparent" '
                    'width="400" height="300" frameborder="0" wmode="Opaque" '
                    'webkitAllowFullScreen mozallowfullscreen '
                    'allowFullScreen></iframe>') % (url.scheme, video_id)

    def save(self):
        if not self.preview:
            self.preview = self.body
        return super(Blog, self).save()

    @property
    def num_comments(self):
        return self.comment_set.count()

    @property
    def images(self):
        return self.blogimage_set.order_by('order', 'pk')

    @property
    def front_images(self):
        return self.blogimage_set.filter(front_page=True).order_by('order', 'pk')


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
    ORDER_CHOICES = zip(*[range(100)]*2)

    title = models.CharField(max_length=128, default='', blank=True)
    blog = models.ForeignKey(Blog)
    image = models.ImageField(upload_to='images')
    front_page = models.BooleanField(default=True)
    order = models.IntegerField(default=0, blank=True, choices=ORDER_CHOICES)
    ext_url = models.URLField(null=True, blank=True, max_length=2048)

    def __init__(self, *args, **kwargs):
        super(BlogImage, self).__init__(*args, **kwargs)
        self._api = requests.Session()
        self._api.headers.update({'Authorization': 'OAuth {}'.format(settings.YANDEX_TOKEN),
                                  'Content-Type': 'application/json; charset=utf-8'})

    def _success_wait(self, response):
        if response.status_code == 202:
            operation_url = response.json()['href']
            while response.json().get('status') != 'success':
                response = self._api.get(operation_url)

    def save_to_yadisk(self):
        method = lambda path: 'https://cloud-api.yandex.net/v1/disk/resources/{}'.format(path)

        # Create blog directory
        resp = self._api.put(method(''), params={'path': self.blog.slug})
        self._success_wait(resp)

        file_name = os.path.basename(self.image.name)
        full_path = u'{}/{}'.format(self.blog.slug, file_name)
        full_url = 'http://{}{}'.format(settings.HOSTNAME, self.image.url)

        # Delete old file
        resp = self._api.delete(method(''), params={'path': full_path, 'permanently': True})
        self._success_wait(resp)

        # Put file to disk
        resp = self._api.post(method('upload'), params={'path': full_path, 'url': full_url, 'disable_redirects': True})
        self._success_wait(resp)

        # Make file public
        resp = self._api.put(method('publish'), params={'path': full_path})
        self._success_wait(resp)

        # Get publick link
        resp = self._api.get(method('download'), params={'path': full_path})

        if resp.status_code == 200:
            self.ext_url = resp.json()['href']
            super(BlogImage, self).save()


    def save(self, *args, **kwargs):
        super(BlogImage, self).save(*args, **kwargs)
        self.save_to_yadisk()


# import the File class to inherit from
from filer.models.filemodels import File as FilerFile

# we'll need to refer to filer settings
from filer import settings as filer_settings

class MediaFile(FilerFile):
    pass


class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    body = RichTextField()
    slug = models.SlugField(max_length=128, unique=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, default=1)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    tags = TaggableManagerN(through=ArticleTaggedItem)

    def __unicode__(self):
        return u'%s' % self.title
