# -*- coding: utf-8 -*-


from django.contrib import admin

from settings import MEDIA_URL
from .models import News, MSettings


class NewsAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug_title', 'pub_date', 'show', 'icon', )
    list_filter = ('pub_date', 'show', )
    search_fields = ('title', 'preview', 'content', )

    def icon(self, obj):
        from sorl.thumbnail import get_thumbnail

        try:
            im = get_thumbnail(obj.image, '60x60', crop='center', quality=99)
            return u'<img src="%s%s" border="0" alt="%s"  align="center" />' % \
                   (MEDIA_URL, im, obj.title)
        except:
            return u'<img src="%sdefault_faq.jpg" border="0" alt="" width="60" height="60" align="center" />' % \
                   (MEDIA_URL)

    prepopulated_fields = {'slug_title': ('title', )}

    icon.short_description = 'Миниатюра'
    icon.allow_tags = True
    icon.admin_order_field = 'title'

    class Media:
        js = [
            '/media/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/media/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(News, NewsAdmin)


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
