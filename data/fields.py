#coding: utf-8
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os
# from mysite import settings

small_width = 216
small_height = 216
medium_width = 512
medium_height = 512

def _add_thumb(s, sgn):
	"""
	Modifies a string (filename, URL) containing an image filename, to insert
	'.thumb'
	"""
	parts = s.split(".")
	parts.insert(-1, "thumb" + sgn)
	if parts[-1].lower() not in ['jpeg', 'jpg']:
		parts[-1] = 'jpg'
	return ".".join(parts)

class ThumbnailImageFieldFile(ImageFieldFile):
	def _get_small_path(self):
		return _add_thumb(self.path, 's')
	small_path = property(_get_small_path)

	def _get_small_url(self):
		return _add_thumb(self.url, 's')
	small_url = property(_get_small_url)

	def _get_medium_path(self):
		return _add_thumb(self.path, 'm')
	medium_path = property(_get_medium_path)

	def _get_medium_url(self):
		return _add_thumb(self.url, 'm')
	medium_url = property(_get_medium_url)

	def save(self, name, content, save=True):
		super(ThumbnailImageFieldFile, self).save(name, content, save)
		img = Image.open(self.path)
		img.thumbnail(
			(small_width, small_height),
			Image.ANTIALIAS,
		)

		img.save(self.small_path, 'JPEG')
		img = Image.open(self.path)
		img.thumbnail(
			(medium_width, medium_height),
			Image.ANTIALIAS,
		)
		img.save(self.medium_path, 'JPEG')

	def delete(self, save=True):
		if os.path.exists(self.small_path):
			os.remove(self.small_path)
		if os.path.exists(self.medium_path):
			os.remove(self.medium_path)
		super(ThumbnailImageFieldFile, self).delete(save)

class ThumbnailImageField(ImageField):
    """
    Behaves like a regular ImageField, but stores an extra (JPEG) thumbnail
    image, providing FIELD.thumb_url and FIELD.thumb_path.
    
    Accepts two additional, optional arguments: thumb_width and thumb_height,
    both defaulting to 128 (pixels). Resizing will preserve aspect ratio while
    staying inside the requested dimensions; see PIL's Image.thumbnail()
    method documentation for details.
    """
    attr_class = ThumbnailImageFieldFile

    def __init__(self, *args, **kwargs):
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
