#coding: utf-8
import hashlib
import datetime, time, os
from django.db import models
from data.fields import ThumbnailImageField
from wetu.settings import MEDIA_ROOT
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

"""
notice:
	1. please ensure that MEDIA_ROOT is declared in setting.py
"""

# default album name
DAN = "default album"
# the directory where users' icons should upload to
IP = "icon"
# the directory where users' images should upload to
UP = "imgdata"
# the entire directory where users' icons should upload to
THP = MEDIA_ROOT + IP + "\\"
# view for user's icon url
Iurl = "album_list"
# view for user's image ulr
Murl = "photo_detail"

# these are just functions.
FK = models.ForeignKey
IF = models.ImageField
TIF = ThumbnailImageField
NBF = models.NullBooleanField
DF = models.DateField
CF = models.CharField
PIF = models.PositiveIntegerField
DTF = models.DateTimeField
AF = models.AutoField
BF = models.BooleanField
O2OF = models.OneToOneField
SF = models.SlugField

def clearOldFile(file):
	if (os.path.exists(file)):
		os.remove(file)

# Create your models here.
class Info(models.Model):
	ID = O2OF(User, related_name = '+', limit_choices_to = {'is_superuser':False}, primary_key = True)
	icon = IF(upload_to = IP, null = True)
	sex = NBF()
	birth = DF(null = True)
	intro = CF(max_length = 255, blank = True)
	addr = CF(max_length = 255, blank = True)
	tools = CF(max_length = 16, blank = True)
	push = PIF(default = 0)
	favor = PIF(default = 0)
	like = PIF(default = 0)
	collect = PIF(default = 0)
	focus = PIF(default = 0)
	inform = PIF(default = 0)
	slug = SF()

	def edit(self, edit):
		"""
		intro:	this method is to edit the information of this user and save
		input:	edit - a dictionary that's in the form like:
					{'Attribute_1':Value_1, 'Attribute_2':Value_2, ...}
		notice:	1.I won't check if you have send an right attribute in
		"""
		for e in edit:
			if e.__eq__('icon'):
				clearOldFile(THP + self.slug)
				self.image.save(self.slug, edit[e])
			else:
				setattr(self, e, edit[e])
		self.save()

	def get_absolute_url(self):
		return reverse(Iurl, args = [self.slug])

class UserTag(models.Model):
	content = CF(max_length = 16, blank = False)
	ID = FK(User, related_name = '+', primary_key = True)
	date = DTF(auto_now_add = True)

class Obj(models.Model):
	pass

class PicsTextTag(models.Model):
	content = CF(max_length = 16, blank = False)
	ID = FK(Obj)
	date = DTF(auto_now_add = True)

class ImageTag(models.Model):
	content = CF(max_length = 16, blank = False)
	ID = FK(Obj)
	date = DTF(auto_now_add = True)

class Album(models.Model):
	ID = FK(Obj, primary_key = True)
	name = CF(max_length = 16, blank = False)
	date = DTF(auto_now_add = True)
	owner = FK(User, related_name = '+')
	intro = CF(max_length = 255, blank = True)
	slug = SF()

	def get_absolute_url(self):
		return reverse('album_detail', kwargs={'slug': self.slug})

	def getInfoSlug(self):
		return Info.objects.filter(ID__id = self.owner.id).first().slug

class Comment(models.Model):
	A = FK(User, related_name = '+')
	B = FK(User, related_name = '+')
	date = DTF(auto_now_add = True)
	content = CF(max_length = 255, blank = False)
	objtype = CF(max_length = 1, blank = False)
	objID = FK(Obj)

class PicsText(models.Model):
	objID = FK(Obj, primary_key = True)
	title = CF(max_length = 16, blank = False)
	owner = FK(User, related_name = '+')
	date = DTF(auto_now_add = True)
	isdraft = BF()
	content = CF(max_length = 21024, blank = False)
	slug = SF()

class Photo(models.Model):
	objID = FK(Obj, primary_key = True)
	name = CF(max_length = 128, blank = False)
	suffix = CF(max_length = 16, null = False)
	intro = CF(max_length = 255)
	image = TIF(upload_to = UP, blank = False)
	isorginal = BF()
	date = DTF(auto_now_add = True)
	inalbum = FK(Album)
	slug = SF()

	class Meta:
		order_with_respect_to = "inalbum"

	def get_absolute_url(self):
		return reverse(Murl, kwargs = {'slug': self.slug})

class Praise(models.Model):
	ID = FK(User, related_name = '+')
	ObjID = FK(Obj)
	date = DTF(auto_now_add = True)

class Message(models.Model):
	A = FK(User, related_name = '+')
	B = FK(User, related_name = '+')
	date = DTF(auto_now_add = True)
	content = CF(max_length = 255, blank = False)

class Focus(models.Model):
	A = FK(User, related_name = '+')
	B = FK(User, related_name = '+')
	date = DTF(auto_now_add = True)
	newMes = PIF(default = 0)

class Collect(models.Model):
	ID = FK(User, related_name = '+')
	objID = FK(Obj)
	date = DTF(auto_now_add = True)

class Favour(models.Model):
	ID = FK(User, related_name = '+')
	objID = FK(Obj)
	date = DTF(auto_now_add = True)

class WaitingPicsText(models.Model):
	ObjID = FK(Obj, primary_key = True)
	date = DTF(auto_now = True)

class CheckedPicsText(models.Model):
	ObjID = FK(Obj, primary_key = True)
	date = DTF(auto_now = True)

class Ated(models.Model):
	commentID = FK(Comment)
	ater = FK(User, related_name = '+')

class Inform(models.Model):
	admin = FK(User, related_name = '+')
	ID = FK(User, related_name = '+')
	content = CF(max_length = 21024)


