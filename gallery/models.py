from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse

from gallery.fields import ThumbnailImageField

class Album(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=40)

    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('album_detail', kwargs={'slug': self.slug})

class Photo(models.Model):
    album = models.ForeignKey(Album)
    title = models.CharField(max_length=100)
    image = ThumbnailImageField(upload_to='photos')
    caption = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=40)
        
    class Meta:
        ordering = ['title']
        order_with_respect_to = 'album'
        
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo_detail', kwargs={'slug': self.slug})

    def get_prev_absolute_url(self):
        pass

    def get_next_absolute_url(self):
        photo = self.get_next_in_order()
        return reverse('photo_detail', kwargs={'slug': photo.slug})

