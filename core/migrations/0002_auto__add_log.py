# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table(u'core_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(default='127.0.0.1', max_length=39)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('method', self.gf('django.db.models.fields.CharField')(default='GET', max_length=4)),
            ('path', self.gf('django.db.models.fields.CharField')(default='/', max_length=255)),
            ('query_get', self.gf('django.db.models.fields.CharField')(default='{}', max_length=512)),
            ('query_post', self.gf('django.db.models.fields.CharField')(default='{}', max_length=512)),
            ('sessionid', self.gf('django.db.models.fields.CharField')(default='', max_length=512)),
            ('http_referer', self.gf('django.db.models.fields.URLField')(default='', max_length=1024)),
            ('http_user_agent', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal(u'core', ['Log'])


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table(u'core_log')


    models = {
        u'core.log': {
            'Meta': {'object_name': 'Log'},
            'http_referer': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '1024'}),
            'http_user_agent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '39'}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'GET'", 'max_length': '4'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '255'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'query_get': ('django.db.models.fields.CharField', [], {'default': "'{}'", 'max_length': '512'}),
            'query_post': ('django.db.models.fields.CharField', [], {'default': "'{}'", 'max_length': '512'}),
            'sessionid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        }
    }

    complete_apps = ['core']