#!-*-coding: utf8-*-
from django import template
from django.utils import simplejson as json

from ..models import Audio

register = template.Library()

@register.simple_tag
def radio_playlist():
    songs = Audio.objects.all()
    playlist = []
    for song in songs:
        playlist.append({
            'id': song.id,
            'aid': song.aid,
            'artist': song.artist,
            'title': song.title,
            'full_title': '%s - %s' % (song.artist, song.title),
            'duration': song.duration,
            'ogg': song.ogg.url,
            'mp3': song.mp3.url
        })

    return json.dumps(playlist)
