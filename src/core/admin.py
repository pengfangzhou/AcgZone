from django.contrib import admin
from django.utils import simplejson as json
from django.utils.translation import ugettext_lazy as _
from models import *

class NoticeshipInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = Noticeship
    fields = ('notice', 'position')
    sortable_field_name = 'position'
    raw_id_fields = ('notice', )
    related_lookup_fields = {
        'fk': ('notice',)
    }
    extra = 0

class ZoneAdmin(admin.ModelAdmin):
    inlines = (NoticeshipInline, )
    list_display = ('zoneid', 'domain', 'maxnum', 'status', 'index')
    search_fields = ('zoneid', 'domain')
    fields = ('zoneid', 'domain', 'maxnum', 'channels', 'status', 'index')
    filter_vertical = ('channels', )

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'version', 'version2', 'version3')
    search_fields = ('title', 'version')
    fields = ('title', 'slug', 'version', 'version2', 'version3')

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'sign')
    search_fields = ('title', )
    fields = ('title', 'content', 'screenshot', 'created_at', 'sign', )

class UpdateAdmin(admin.ModelAdmin):
    list_display = ('channel', 'url', 'cversion', 'tversion', 'sign')
    search_fields = ('cversion', 'tversion')
    fields = ('channel', 'url', 'cversion', 'tversion', 'sign')

class UpgradeAdmin(admin.ModelAdmin):
    list_display = ('channel', 'version', 'url', 'md5')
    search_fields = ('version', 'url')
    fields = ('channel', 'version', 'url', 'md5')

admin.site.register(Zone, ZoneAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Update, UpdateAdmin)
admin.site.register(Upgrade, UpgradeAdmin)