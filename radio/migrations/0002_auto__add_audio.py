# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Audio'
        db.create_table(u'radio_audio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aid', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=128, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='No title', max_length=128, blank=True)),
            ('lyrics_id', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('genre', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'radio', ['Audio'])


    def backwards(self, orm):
        # Deleting model 'Audio'
        db.delete_table(u'radio_audio')


    models = {
        u'radio.audio': {
            'Meta': {'object_name': 'Audio'},
            'aid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'genre': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lyrics_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'No title'", 'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['radio']