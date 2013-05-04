#-*-coding: utf8-*-
from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    METHODS = (
        ('GET', 'GET'),
        ('POST', 'POST'),
    )

    ip = models.GenericIPAddressField(default='127.0.0.1')
    port = models.IntegerField(default=0)
    method = models.CharField(default='GET', choices=METHODS, max_length=4)
    path = models.CharField(default='/', max_length=255)
    query_get = models.CharField(default='{}', max_length=512)
    query_post = models.CharField(default='{}', max_length=512)
    sessionid = models.CharField(default='', max_length=512)
    http_referer = models.URLField(max_length=1024, default='')
    http_user_agent = models.CharField(default='', max_length=255)
    user = models.ForeignKey(User, default=None, null=True, blank=True)
