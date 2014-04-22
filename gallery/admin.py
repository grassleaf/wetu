from django.contrib import admin
from .models import Album, Photo

# Register your models here.


class PhotoInline(admin.StackedInline):
    model = Photo

class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

admin.site.register(Album, AlbumAdmin)    
admin.site.register(Photo)