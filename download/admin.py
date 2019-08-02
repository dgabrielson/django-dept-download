from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from download.models import Download_File, History_Record, Platform, Software


class History_RecordOptions(admin.ModelAdmin):
    list_display = ['when', 'user', 'software']
    list_filter = [
        'when',
        'software',
    ]
    search_fields = [
        'user__username',
    ]


class PlatformOptions(admin.ModelAdmin):
    list_display = [
        'slug',
        'Name',
    ]


class Download_FileOptions(admin.ModelAdmin):
    list_display = [
        'slug',
        'Name',
        'software',
        'platform',
        'filename',
    ]


class SoftwareOptions(admin.ModelAdmin):
    list_display = [
        'slug',
        'Name',
    ]


admin.site.register(History_Record, History_RecordOptions)
admin.site.register(Platform, PlatformOptions)
admin.site.register(Download_File, Download_FileOptions)
admin.site.register(Software, SoftwareOptions)
