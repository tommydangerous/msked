# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Seat'
        db.create_table('seats_seat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stations.Station'])),
        ))
        db.send_create_signal('seats', ['Seat'])

        # Adding unique constraint on 'Seat', fields ['name', 'station']
        db.create_unique('seats_seat', ['name', 'station_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Seat', fields ['name', 'station']
        db.delete_unique('seats_seat', ['name', 'station_id'])

        # Deleting model 'Seat'
        db.delete_table('seats_seat')


    models = {
        'seats.seat': {
            'Meta': {'unique_together': "(('name', 'station'),)", 'object_name': 'Seat'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stations.Station']"})
        },
        'stations.station': {
            'Meta': {'object_name': 'Station'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['seats']