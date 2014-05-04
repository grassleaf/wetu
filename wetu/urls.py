#coding:utf-8
from django.conf.urls import patterns, include, url
from wetu import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zhaoqu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'', include('accounts.urls')),
    url(r'', include('gallery.urls')),
    url(r'^crawl/', include('crawl.urls')),
)

urlpatterns += patterns('',
	# url(r"^static/(?P<path>.*)$", "django.views.static.serve", \
 #        {"document_root": '/home/michael/workspace/web/wetu/static'}),
	url(r"^media/(?P<path>.*)$", "django.views.static.serve", \
        {"document_root": settings.MEDIA_ROOT}),
)