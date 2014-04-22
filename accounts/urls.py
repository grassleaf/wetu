#coding: utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('accounts.views',
	url(r'^register/$', 'register'),
	url(r'^login/$', 'login'),
	url(r'^logout/$', 'logout'),
)