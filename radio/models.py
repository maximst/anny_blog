from django.db import models


class Audio(models.Model):
    aid = models.IntegerField(unique=True)
    artist = models.CharField(max_length=128, blank=True, default='Unknown')
    title = models.CharField(max_length=128, blank=True, default='No title')
    lyrics_id = models.CharField(max_length=32, blank=True, null=True)
    genre = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    file = models.FileField(upload_to='radio')
