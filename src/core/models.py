# -*- coding: utf-8 -*-
import datetime
import hashlib
from django.db import models
from django.utils.text import ugettext_lazy as _
from cyclone import escape
from positions import PositionField
from signals import *
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ValidationError
from filebrowser.fields import FileBrowseField, FileObject

class Member(models.Model):
    memberid = models.AutoField(primary_key=True)
    username = models.CharField(_('Username'), max_length=50, unique=True)
    password = models.CharField(_('Password'), max_length=200,)
    clientid = models.CharField(_('Clientid'), max_length=100, blank=True)
    clientsecret = models.CharField(_('Clientsecret'), max_length=100, blank=True)
    channel = models.CharField(_('Channel'), max_length=100, blank=True)
    realchannel = models.CharField(_('Realchannel'), max_length=100, blank=True)
    udid = models.CharField(_('Udid'), max_length=100, blank=True)
    authstring = models.CharField(_('Authstring'), max_length=200, blank=True)
    source = models.CharField(_('Source'), max_length=50, blank=True)
    phone = models.CharField(_('Phone'), max_length=100, blank=True)
    model = models.CharField(_('Model'), max_length=200, blank=True)
    serial = models.CharField(_('Serial'), max_length=200, blank=True)
    ip = models.CharField(_('Ip'), max_length=100, blank=True)
    msg = models.CharField(_('Msg'), max_length=300, blank=True)
    fronttime = models.CharField(_('Fronttime'), max_length=200, blank=True)
    created = models.PositiveIntegerField(_('Created'), default=0)
    updated = models.PositiveIntegerField(_('Updated'), default=0)
    question = models.CharField(_('Question'), max_length=200, blank=True)
    answer = models.CharField(_('Answer'), max_length=200, blank=True)

class Zone(models.Model):
    FULL = 0
    NEWAREA = 1
    KEEP = 2
    STATUS = (
        (FULL, _('Full')),
        (NEWAREA, _('NewArea')),
        (KEEP, _('Keep')),
    )
    zoneid = models.PositiveIntegerField(_('Zoneid'), default=0)
    index = models.CharField(_('Index'), max_length=10)
    domain = models.CharField(_('Domain'), max_length=100, blank=True)
    maxnum = models.PositiveIntegerField(_('Maxnum'), default=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    channels = models.ManyToManyField('Channel', blank=True)
    # notices = models.ManyToManyField('Notice', blank=True)
    notices = models.ManyToManyField('Notice', through='Noticeship', blank=True)
    status = models.PositiveSmallIntegerField(
        _('Status'), choices=STATUS, default=KEEP)

    class Meta:
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')

    def __unicode__(self):
        return ':'.join([self.domain, str(self.zoneid)])

class Channel(models.Model):
    title = models.CharField(_('Title'), max_length=20, unique=True)
    slug = models.SlugField(_('Slug'))
    version = models.CharField(_('Max_version1'), max_length=64, editable=True)
    version2 = models.CharField(_('Max_version2'), max_length=64, editable=True)
    version3 = models.CharField(_('Max_version3'), max_length=64, editable=True)

    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')
        ordering = ('slug',)

    def __unicode__(self):
        return self.title

class Notice(models.Model):
    title = models.CharField(_('Title'), max_length=20, unique=True)
    content = models.TextField(blank=True)
    screenshot = FileBrowseField(_('Screenshot'), max_length=200, directory='img/screenshot', format='image', extensions=[".jpg"], blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    sign = models.CharField(_('Sign'), max_length=20, blank=True)

    class Meta:
        verbose_name = _('Notice')
        verbose_name_plural = _('Notices')

    def __unicode__(self):
        return self.title

    def clean_fields(self, exclude=None):
        super(Notice, self).clean_fields()

        if self.screenshot and not self.screenshot.exists():
            raise ValidationError({'file': [_('File Not Exists')]})
        else:
            path = self.screenshot.site.storage.path(self.screenshot)
            m = hashlib.md5()
            a_file = open(path, 'rb')
            m.update(a_file.read())
            self.sign = m.hexdigest()

class Noticeship(models.Model):
    zone = models.ForeignKey(Zone)
    notice = models.ForeignKey(Notice)
    position = PositionField(_('Position'), collection='zone')

    class Meta:
        verbose_name = 'Noticeship'
        verbose_name_plural = _('Noticeships')
        ordering = ('position', )

    def __unicode__(self):
        return self.notice.title

class Update(models.Model):
    channel = models.ForeignKey(Channel)
    cversion = models.CharField(_('Cur_version'), max_length=64, editable=True)
    tversion = models.CharField(_('Tar_version'), max_length=64, editable=True)
    url = models.URLField()
    # file = FileBrowseField(
    #     _('File'), max_length=200, directory='update', extensions=[".zip"],
    #     blank=True
    # )
    sign = models.CharField(_('Md5'), max_length=64, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Update')
        verbose_name_plural = _('Updates')

    def __unicode__(self):
        return 'version %s to %s' % (self.cversion, self.tversion)

class Upgrade(models.Model):
    channel = models.ForeignKey(Channel)
    version = models.CharField(_('Version'), max_length=64, editable=True)
    url = models.URLField()
    md5 = models.CharField(_('Md5'), max_length=64, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Upgrade')
        verbose_name_plural = _('Upgrades')

    def __unicode__(self):
        return 'version %s' % self.version

class BindToken(models.Model):
    channel = models.ForeignKey(Channel)
    thirdparty_token = models.CharField(_('Thirdparty_token'), max_length=128, editable=True)
    access_token = models.CharField(_('Access_token'), max_length=128, editable=True)
    timestamp = models.PositiveIntegerField(_('Timestamp'), default=0, blank=True)
    
    class Meta:
        verbose_name = _('BindToken')
        verbose_name_plural = _('BindTokens')
        unique_together = (('channel', 'thirdparty_token'),)

    def __unicode__(self):
        return 'token %s' % self.access_token
