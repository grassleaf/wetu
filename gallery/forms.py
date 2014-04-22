#coding: utf-8
from django import forms
from django.db import models
from gallery.models import Item
from gallery.fields import ThumbnailImageField

class ItemForm(forms.Form):
    name = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=40)

class PhotoForm(forms.Form):
    item = models.ForeignKey(Item)
    title = models.CharField(max_length=100)
    image = ThumbnailImageField(upload_to='photos')
    caption = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=40)
