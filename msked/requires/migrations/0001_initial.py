# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Require'
        db.create_table('requires_require', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employees.Employee'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Job'])),
        ))
        db.send_create_signal('requires', ['Require'])

        # Adding unique constraint on 'Require', fields ['employee', 'job']
        db.create_unique('requires_require', ['employee_id', 'job_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Require', fields ['employee', 'job']
        db.delete_unique('requires_require', ['employee_id', 'job_id'])

        # Deleting model 'Require'
        db.delete_table('requires_require')


    models = {
        'employees.employee': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Employee'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'floater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']", 'null': 'True', 'blank': 'True'}),
            'tier_lab': ('django.db.models.fields.IntegerField', [], {}),
            'tier_office': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'daily': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']", 'null': 'True', 'blank': 'True'}),
            'weekly': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'requires.require': {
            'Meta': {'unique_together': "(('employee', 'job'),)", 'object_name': 'Require'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employees.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Job']"})
        },
        'teams.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['requires']