# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UpdateMessage.status'
        db.add_column('update_messages_updatemessage', 'status',
                      self.gf('django.db.models.fields.CharField')(default='warning', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UpdateMessage.status'
        db.delete_column('update_messages_updatemessage', 'status')


    models = {
        'update_messages.updatemessage': {
            'Meta': {'object_name': 'UpdateMessage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'warning'", 'max_length': '255'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['update_messages']