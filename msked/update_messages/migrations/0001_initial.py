# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UpdateMessage'
        db.create_table('update_messages_updatemessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('update_messages', ['UpdateMessage'])


    def backwards(self, orm):
        # Deleting model 'UpdateMessage'
        db.delete_table('update_messages_updatemessage')


    models = {
        'update_messages.updatemessage': {
            'Meta': {'object_name': 'UpdateMessage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['update_messages']