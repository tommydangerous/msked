# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Exclude.job'
        db.alter_column('excludes_exclude', 'job_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Job'], null=True))
        # Adding unique constraint on 'Exclude', fields ['job', 'team']
        db.create_unique('excludes_exclude', ['job_id', 'team_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Exclude', fields ['job', 'team']
        db.delete_unique('excludes_exclude', ['job_id', 'team_id'])


        # Changing field 'Exclude.job'
        db.alter_column('excludes_exclude', 'job_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['jobs.Job']))

    models = {
        'excludes.exclude': {
            'Meta': {'unique_together': "(('job', 'team'),)", 'object_name': 'Exclude'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Job']", 'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']"})
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
        'teams.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['excludes']