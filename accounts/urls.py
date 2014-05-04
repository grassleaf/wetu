#coding: utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from data.models import Album
from django.views.generic import ListView

urlpatterns = patterns('accounts.views',
	url(r'^register/$', 'register'),
	url(r'^login/$', 'login'),
	url(r'^logout/$', 'logout'),
)

urlpatterns += patterns('django.views.generic',
	url(r'^people/(?P<slug>[-_\w]+)$', ListView.as_view(model=Album,
        template_name='home.html'),
        name='home'
    ),
)