#!-*-coding: utf8-*-
from django import template
import json

from ..models import Audio

from core.templatetags.coretags import ext_media

register = template.Library()

@register.simple_tag
def radio_playlist():
    songs = Audio.objects.all().order_by('?')
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
            'mp3': song.mp3.url,
            'ext_ogg': ext_media(song.ogg.url),
            'ext_mp3': ext_media(song.mp3.url),
        })

    return json.dumps(playlist)#, indent=4)
