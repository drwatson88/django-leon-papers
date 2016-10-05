# -*- coding: utf-8 -*-

from django.contrib import admin
from treebeard.admin import TreeAdmin
from settings import MEDIA_URL

from models import Portfolio, Category, MSettings

class CategoryAdmin(TreeAdmin):
	list_display = ('title','icon','show', )
	list_filter  = ('parent', 'show',)
	search_fields = ('title', 'anonce',)

	class Media:
		js = [
			'/media/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
			'/media/grappelli/tinymce_setup/tinymce_setup.js',
		]
 
	def icon(self, obj):
		from sorl.thumbnail import get_thumbnail

		try :
			im = get_thumbnail(obj.image, '60x60', crop='center', quality=99)
			return u'<img src="%s%s" border="0" alt="%s"  align="center" />' % \
			       (MEDIA_URL, im, obj.title)
		except :
			return u'<img src="%sdefault_faq.jpg" border="0" alt="" width="60" height="60" align="center" />' % \
			       (MEDIA_URL)

	icon.short_description = 'Миниатюра'
	icon.allow_tags = True
	icon.admin_order_field = 'title'
	prepopulated_fields = {'slug_title': ('title', ) }
  
admin.site.register(Category, CategoryAdmin)

class PortfolioAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date', 'category', 'show', 'icon','position',)
	list_filter  = ('pub_date', 'show', 'category', )
	search_fields = ('title', 'preview', 'content', )
	list_editable = ('position',)
  	
	def icon(self, obj):
		from sorl.thumbnail import get_thumbnail

		try :
			im = get_thumbnail(obj.image, '60x60', crop='center', quality=99)
			return u'<img src="%s%s" border="0" alt="%s"  align="center" />' % \
			       (MEDIA_URL, im, obj.title)
		except :
			return u'<img src="%sdefault_faq.jpg" border="0" alt="" width="60" height="60" align="center" />' % \
			       (MEDIA_URL)

	prepopulated_fields = {'slug_title': ('title', ) }

	icon.short_description = 'Миниатюра'
	icon.allow_tags = True
	icon.admin_order_field = 'title'

	class Media:
		js = [
			'/media/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
			'/media/grappelli/tinymce_setup/tinymce_setup.js',
      '/media/js/admin_list_reorder.js',
		]

admin.site.register(Portfolio, PortfolioAdmin)

class MSettingsAdmin(admin.ModelAdmin):
	list_display = ('title', )
	
	class Media:
		js = [
			'/media/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
			'/media/grappelli/tinymce_setup/tinymce_setup.js',
		]  	
	
	def has_delete_permission(self, request, obj=None):
		if obj is not None: 
			if obj.id==1:
				return False
		return super(MSettingsAdmin, self).has_delete_permission(request, obj=obj)
		
admin.site.register(MSettings, MSettingsAdmin)		