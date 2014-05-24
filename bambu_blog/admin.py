from django.contrib import admin
from django.contrib.admin.helpers import AdminForm, InlineAdminFormSet, AdminErrorList
from django.conf import settings
from django.conf.urls import patterns
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from bambu_blog.models import *
from bambu_blog.forms import PostForm
from bambu_attachments.admin import AttachmentInline

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'published')
    list_filter = ('published', 'categories')
    date_hierarchy = 'date'
    prepopulated_fields = {
        'slug': ('title',)
    }
    
    search_fields = ('title', 'body')
    form = PostForm
    
    fieldsets = (
        (
            u'Basics',
            {
                'fields': ('title', 'date', 'published')
            }
        ),
        (
            u'Post content',
            {
                'fields': ('body',)
            }
        ),
        (
            u'Metadata',
            {
                'fields': ('slug', 'author', 'tags', 'categories'),
                'classes': ('collapse', 'closed')
            }
        ),
        (
            u'Advanced',
            {
                'fields': ('css',)
            }
        )
    )

    inlines = (AttachmentInline,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user

        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    class Media:
        js = 'grappelli' in settings.INSTALLED_APPS and (
            'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'js/tinymce_setup.js'
        ) or ()

admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }

admin.site.register(Category, CategoryAdmin)
