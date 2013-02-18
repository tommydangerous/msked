# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Employee.slug'
        db.add_column('employees_employee', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Employee', fields ['first_name', 'last_name']
        db.create_unique('employees_employee', ['first_name', 'last_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Employee', fields ['first_name', 'last_name']
        db.delete_unique('employees_employee', ['first_name', 'last_name'])

        # Deleting field 'Employee.slug'
        db.delete_column('employees_employee', 'slug')


    models = {
        'employees.employee': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Employee'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'floater': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']", 'null': 'True', 'blank': 'True'}),
            'tier_lab': ('django.db.models.fields.IntegerField', [], {}),
            'tier_office': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teams.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['employees']