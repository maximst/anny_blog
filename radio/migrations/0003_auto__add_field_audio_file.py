# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Audio.file'
        db.add_column(u'radio_audio', 'file',
                      self.gf('django.db.models.fields.files.FileField')(default='default.ogg', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Audio.file'
        db.delete_column(u'radio_audio', 'file')


    models = {
        u'radio.audio': {
            'Meta': {'object_name': 'Audio'},
            'aid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'genre': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lyrics_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'No title'", 'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['radio']