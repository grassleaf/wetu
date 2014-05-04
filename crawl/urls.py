#coding:utf-8
from django.conf.urls import patterns, include, url
from wetu import settings

urlpatterns = patterns('crawl.views',
	url(r'^issue/$', 'issue'),
)