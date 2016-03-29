# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table(u'core_member', (
            ('memberid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('clientid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('clientsecret', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('realchannel', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('udid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('authstring', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('fronttime', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('created', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('updated', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Member'])

        # Adding model 'Zone'
        db.create_table(u'core_zone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zoneid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('index', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('maxnum', self.gf('django.db.models.fields.PositiveIntegerField')(default=2000)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
        ))
        db.send_create_signal(u'core', ['Zone'])

        # Adding M2M table for field channels on 'Zone'
        m2m_table_name = db.shorten_name(u'core_zone_channels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('zone', models.ForeignKey(orm[u'core.zone'], null=False)),
            ('channel', models.ForeignKey(orm[u'core.channel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['zone_id', 'channel_id'])

        # Adding model 'Channel'
        db.create_table(u'core_channel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('version2', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('version3', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'core', ['Channel'])

        # Adding model 'Notice'
        db.create_table(u'core_notice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('screenshot', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'core', ['Notice'])

        # Adding model 'Noticeship'
        db.create_table(u'core_noticeship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Zone'])),
            ('notice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Notice'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal(u'core', ['Noticeship'])

        # Adding model 'Update'
        db.create_table(u'core_update', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Channel'])),
            ('cversion', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('tversion', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Update'])

        # Adding model 'Upgrade'
        db.create_table(u'core_upgrade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Channel'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Upgrade'])

        # Adding model 'BindToken'
        db.create_table(u'core_bindtoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Channel'])),
            ('thirdparty_token', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('timestamp', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'core', ['BindToken'])

        # Adding unique constraint on 'BindToken', fields ['channel', 'thirdparty_token']
        db.create_unique(u'core_bindtoken', ['channel_id', 'thirdparty_token'])


    def backwards(self, orm):
        # Removing unique constraint on 'BindToken', fields ['channel', 'thirdparty_token']
        db.delete_unique(u'core_bindtoken', ['channel_id', 'thirdparty_token'])

        # Deleting model 'Member'
        db.delete_table(u'core_member')

        # Deleting model 'Zone'
        db.delete_table(u'core_zone')

        # Removing M2M table for field channels on 'Zone'
        db.delete_table(db.shorten_name(u'core_zone_channels'))

        # Deleting model 'Channel'
        db.delete_table(u'core_channel')

        # Deleting model 'Notice'
        db.delete_table(u'core_notice')

        # Deleting model 'Noticeship'
        db.delete_table(u'core_noticeship')

        # Deleting model 'Update'
        db.delete_table(u'core_update')

        # Deleting model 'Upgrade'
        db.delete_table(u'core_upgrade')

        # Deleting model 'BindToken'
        db.delete_table(u'core_bindtoken')


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
        u'core.member': {
            'Meta': {'object_name': 'Member'},
            'authstring': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'clientid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'clientsecret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'fronttime': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'memberid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'realchannel': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'udid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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