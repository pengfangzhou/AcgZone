# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Member'
        db.delete_table(u'core_member')


    def backwards(self, orm):
        # Adding model 'Member'
        db.create_table(u'core_member', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('clientsecret', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('updated', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('udid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('fronttime', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('memberid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clientid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('authstring', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('realchannel', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'core', ['Member'])


    models = {
        u'core.bindtoken': {
            'Meta': {'unique_together': "(('channel', 'thirdparty_token'),)", 'object_name': 'BindToken'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Channel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thirdparty_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'core.channel': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Channel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'version2': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'version3': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'core.notice': {
            'Meta': {'object_name': 'Notice'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'screenshot': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'blank': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'core.noticeship': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Noticeship'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Notice']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Zone']"})
        },
        u'core.update': {
            'Meta': {'object_name': 'Update'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Channel']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cversion': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tversion': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'core.upgrade': {
            'Meta': {'object_name': 'Upgrade'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Channel']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'core.zone': {
            'Meta': {'object_name': 'Zone'},
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Channel']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'maxnum': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2000'}),
            'notices': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Notice']", 'symmetrical': 'False', 'through': u"orm['core.Noticeship']", 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'zoneid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['core']