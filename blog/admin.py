#coding:utf-8
from django.contrib import admin

from .models import Post
from .models import Category
from .models import Widget

class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    fields = ('title', 'category', 'tags', 'content', 'summary', 'status', 'publish_time', 'slug')
    list_display = ('preview', 'title', 'category', 'publish_time')
    ordering = ('-publish_time', )
    save_on_top = True

    def preview(self, obj):
        return u'''
                    <span><a href="%s" target="_blank">预览</a></span>
                    <span><a href="/admin/blog/post/%s/" target="_blank">编辑</a></span>
                ''' % (obj.get_absolute_url(), obj.id)

    preview.short_description = u'操作'
    preview.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if not obj.summary:
            obj.summary = obj.content
        obj.save()

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'create_time')

class WidgetAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    fields = ('title', 'content', 'rank', 'hide')
    list_display = ('title', 'rank', 'hide')

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Widget, WidgetAdmin)