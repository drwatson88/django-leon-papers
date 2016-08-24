# -*- coding: utf-8 -*-


from django.contrib import admin

from settings import MEDIA_URL

from .models import Contact, MSettings


class ContactAdmin(admin.ModelAdmin):

    list_display = ('name', 'message', 'pub_date',)
    list_filter = ('pub_date',)
    search_fields = ('name', 'message',)

admin.site.register(Contact, ContactAdmin)


class MSettingsAdmin(admin.ModelAdmin):

    list_display = ('title', )

    class Media:
        js = [
            '/media/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/media/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if obj.id == 3:
                return False
        return super(MSettingsAdmin, self).has_delete_permission(request, obj=obj)

admin.site.register(MSettings, MSettingsAdmin)
