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
    ogg = models.FileField(upload_to=DIR)
    mp3 = models.FileField(upload_to=DIR)
    url = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        app_label = 'radio'

    def delete(self, *args, **kwargs):
        ogg_storage, ogg_path = self.ogg.storage, self.ogg.path
        mp3_storage, mp3_path = self.mp3.storage, self.mp3.path

        super(Audio, self).delete(*args, **kwargs)

        ogg_storage.delete(ogg_path)
        mp3_storage.delete(mp3_path)
        try:
            os.remove(ogg_path)
            os.remove(mp3_path)
        except OSError:
            pass

    @classmethod
    def file_dir(cls):
        return os.path.join(settings.MEDIA_ROOT, cls.DIR)

    def player(self):
        if self.ogg:
            return u'<audio id="%i" src="%s" controls preload="metadata"></audio>' % (self.id, self.ogg.url)
        else:
            return u'none'

    player.short_description = 'Play'
    player.allow_tags = True
