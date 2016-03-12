# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LEAVE_EVENTS'
        db.create_table('cal_leave_events', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('snippet', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(max_length=400, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('start_time', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('end_time', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('remind', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cal', ['LEAVE_EVENTS'])

        # Adding model 'ORGANISATIONS'
        db.create_table('cal_organisations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('organisation_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('cal', ['ORGANISATIONS'])

        # Adding model 'ADDRESSES'
        db.create_table('cal_addresses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('address_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('house_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('cal', ['ADDRESSES'])

        # Adding model 'TEAMS'
        db.create_table('cal_teams', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('team_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('organisation_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.ORGANISATIONS'], null=True, blank=True)),
        ))
        db.send_create_signal('cal', ['TEAMS'])


    def backwards(self, orm):
        # Deleting model 'LEAVE_EVENTS'
        db.delete_table('cal_leave_events')

        # Deleting model 'ORGANISATIONS'
        db.delete_table('cal_organisations')

        # Deleting model 'ADDRESSES'
        db.delete_table('cal_addresses')

        # Deleting model 'TEAMS'
        db.delete_table('cal_teams')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cal.addresses': {
            'Meta': {'object_name': 'ADDRESSES'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'address_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'house_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'cal.leave_events': {
            'Meta': {'object_name': 'LEAVE_EVENTS'},
            'body': ('django.db.models.fields.TextField', [], {'max_length': '400', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'snippet': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'cal.organisations': {
            'Meta': {'object_name': 'ORGANISATIONS'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        'cal.teams': {
            'Meta': {'object_name': 'TEAMS'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.ORGANISATIONS']", 'null': 'True', 'blank': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cal']