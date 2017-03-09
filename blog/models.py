#-*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField
from hvad.models import TranslatableModel, TranslatedFields

from tag.models import ArticleTaggedItem, TaggableManagerN
from poll.models import Poll
from core.utils import flip_horizontal

from urlparse import urlparse, parse_qs


class Blog(TranslatableModel):
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

    translations = TranslatedFields(
        title = models.CharField(max_length=128),
        preview = models.TextField(default='', blank=True),
        body = models.TextField(default=''),
    )

    name = models.CharField(max_length=128, unique=False)

#    title = models.CharField(max_length=128, unique=True)
#    preview = models.TextField(default='', blank=True)
#    body = models.TextField(default='')
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
    image = models.ImageField(upload_to='images', max_length=1024)
    front_page = models.BooleanField(default=True)
    order = models.IntegerField(default=0, blank=True, choices=ORDER_CHOICES)
    ext_url = models.URLField(null=True, blank=True, max_length=2048)

    def save(self, *args, **kwargs):
#        flip_image = self.id is None
        super(BlogImage, self).save(*args, **kwargs)
#        if flip_image:
#            flip_horizontal(self.image.path)


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
