#coding: utf-8
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from markupfield.fields import MarkupField
import hashlib, time

from wetu import settings

STATUS = {
	0: u'正常',
	1: u'草稿',
	2: u'删除',
}

class Category(models.Model):
	name = models.CharField(max_length=40, verbose_name=u'名称')
	desc = models.CharField(max_length=100, verbose_name=u'描述')

	create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
	update_time = models.DateTimeField(u'更新时间', auto_now=True)
	slug = models.SlugField(max_length=40)

	def __unicode__(self):
		return '%s' % self.name

	class Meta:
		ordering = ['-create_time']
		verbose_name_plural = verbose_name = u"分类" #声明复数形式

	def get_absolute_url(self):
		# return '%s/%s' % (settings.DOMAIN, self.slug)
		# return '%s' % self.slug
		return reverse('category_list', kwargs={'slug': self.slug})

	@classmethod
	def available_list(cls):
		return cls.objects.all() # 使用类方法获取所有objects，相当调用Category.objects.all()

class Post(models.Model):
	"""docstring for Post"""
	author = models.ForeignKey(User, verbose_name=u'作者')
	category = models.ForeignKey(Category, verbose_name=u'分类')
	tags = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'标签', help_text=u'用英文逗号隔开')

	title = models.CharField(max_length=40, verbose_name=u'标题')
	summary = models.TextField(verbose_name=u'摘要')
	# content_rst = models.TextField(verbose_name=u'文章正文rst格式')
	# content_html = models.TextField(verbose_name=u'文章正文html格式', editable=False)
	content = MarkupField(default_markup_type='restructuredtext', verbose_name=u'文章正文')
	view_times = models.IntegerField(default=1)

	create_time = models.DateTimeField(u'创建时间', auto_now_add=True, editable=True)
	publish_time = models.DateTimeField(default=datetime.now(), verbose_name=u'发布时间')
	update_time = models.DateTimeField(u'更新时间', auto_now=True)
	status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name=u'状态')
	slug = models.SlugField(max_length=40)
	
	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-publish_time']
		verbose_name_plural = verbose_name = '文章'

	def tags_list(self):
		return [tag.strip() for tag in self.tags.split(',')]

	def get_absolute_url(self):
		# return '%s/%s' % (settings.DOMAIN, self.slug)
		# return '/%s/%s' % ('article', self.slug)
		return reverse('post_detail', kwargs={'slug': self.slug})

	@classmethod
	def get_recently_posts(cls, num): # 获取num篇最新文章
		return cls.objects.filter(status=0).order_by('-publish_time')[:num]

class Widget(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')

    content = models.TextField(verbose_name=u'widget内容', help_text=u'html代码不会被转义')
    hide = models.BooleanField(default=False, verbose_name=u'隐藏')

    rank = models.IntegerField(default=0, verbose_name=u'展示排序')

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def __unicode__(self):
        return self.title

    @classmethod
    # @cache_decorator(1*60)
    def available_list(cls):
        return cls.objects.filter(hide=False)

    class Meta:
        ordering = ['rank', '-create_time']
        verbose_name_plural = verbose_name = u"侧栏组件"

def getSlug(ID):
	""" intro: get the slug in string form """
	pre = str(hashlib.md5(str(ID)).hexdigest())
	return pre[:6] + str(int(time.time() * 100))