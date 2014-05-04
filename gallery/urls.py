from django.conf.urls import *
from data.models import Album, Photo
from django.views.generic import TemplateView, DetailView, ListView
from gallery.views import IndexView

urlpatterns = patterns('django.views.generic',
    url(r'^$', IndexView.as_view(),
        name = 'index'
    ),
    url(r'^album/$', ListView.as_view(queryset=Album.objects.all(),
        context_object_name='object_list', template_name='album_list.html'),
        name='album_list'
    ),
    url(r'^album/(?P<slug>[-_\w]+)/$', DetailView.as_view(model=Album,
        template_name='album_detail.html'),
        name='album_detail'
    ),
    url(r'^photo/(?P<slug>[-_\w]+)/detail/$', DetailView.as_view(model=Photo,
        template_name='photo_detail.html'),
        name='photo_detail'
    ),
)

urlpatterns += patterns('gallery.views',
    url(r'^upload/$', 'upload'),
    url(r'^create_album/$', 'create_album'),
    url(r'request_albums/(\d+)/$', 'request_albums'),
)
