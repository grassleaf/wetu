#coding: utf-8
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from blog.views import IndexView, CategoryListView, PostDetailView

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', IndexView.as_view(), name='home'),
	url(r'^category/(?P<slug>[-_\w]+)/$', CategoryListView.as_view(), name='category_list'),
	url(r'^article/(?P<slug>[-_\w]+)/$', PostDetailView.as_view(), name='post_detail'),
)

urlpatterns += patterns('blog.views',
	# url(r'^validate_input/$', 'validate_input'),
	url(r'^upload/$', 'upload'),
	url(r'^create_album/$', 'create_album'),
) 
# + static(r'^register/(?P<path>.*)$', document_root=settings.SITEPAGE_ROOT)

urlpatterns += patterns('',
	url(r'^register/(?P<path>.*)$','django.views.static.serve',\
		{'document_root': settings.SITEPAGE_ROOT}),
)