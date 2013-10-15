from django.db import models
from django.conf import settings
import os


class Audio(models.Model):
    DIR = 'radio'

    aid = models.IntegerField(unique=True)
    artist = models.CharField(max_length=128, blank=True, default='Unknown')
    title = models.CharField(max_length=128, blank=True, default='No title')
    lyrics_id = models.CharField(max_length=32, blank=True, null=True)
    genre = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    file = models.FileField(upload_to=DIR)

    class Meta:
        app_label = 'radio'

    @classmethod
    def file_dir(cls):
        return os.path.join(settings.MEDIA_ROOT, cls.DIR)
