# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Employee'
        db.create_table('employees_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('floater', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.Team'], null=True, blank=True)),
            ('tier_lab', self.gf('django.db.models.fields.IntegerField')()),
            ('tier_office', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('vacation', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('employees', ['Employee'])


    def backwards(self, orm):
        # Deleting model 'Employee'
        db.delete_table('employees_employee')


    models = {
        'employees.employee': {
            'Meta': {'object_name': 'Employee'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'floater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']", 'null': 'True', 'blank': 'True'}),
            'tier_lab': ('django.db.models.fields.IntegerField', [], {}),
            'tier_office': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'vacation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teams.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['employees']