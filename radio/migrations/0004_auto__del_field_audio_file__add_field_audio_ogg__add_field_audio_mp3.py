# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Audio.file'
        db.delete_column(u'radio_audio', 'file')

        # Adding field 'Audio.ogg'
        db.add_column(u'radio_audio', 'ogg',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Audio.mp3'
        db.add_column(u'radio_audio', 'mp3',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Audio.file'
        db.add_column(u'radio_audio', 'file',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'Audio.ogg'
        db.delete_column(u'radio_audio', 'ogg')

        # Deleting field 'Audio.mp3'
        db.delete_column(u'radio_audio', 'mp3')


    models = {
        'radio.audio': {
            'Meta': {'object_name': 'Audio'},
            'aid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'genre': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lyrics_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'ogg': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'No title'", 'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['radio']