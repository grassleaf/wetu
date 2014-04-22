from django.views.generic import TemplateView, DetailView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.files.base import ContentFile

from data.models import Album, Photo
from data.func import *

# class AlbumListView(ListView):
#     model = Album
#     context_object_name = 'object_list'
#     template_name = "album_list.html"

#     def get_context_data(self, **kwargs):
#         context = super(AlbumListView, self).get_context_data(**kwargs)
#         return context

#     # def get_queryset(self):
#     #     queryset = super(AlbumListView, self).get_queryset()
#     #     return queryset

# class AlbumDetailView(DetailView):
#     model = Album
#     context_object_name = 'object'
#     template_name = "album_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super(AlbumDetailView, self).get_context_data(**kwargs)
#         return context

#     # def get_object(self, queryset=None):
#     #     return super(AlbumDetailView, self).get_object()

# class PhotoDetailView(DetailView):
#     model = Photo
#     context_object_name = 'object'
#     template_name = "photo_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super(PhotoDetailView, self).get_context_data(**kwargs)
#         return context

@csrf_exempt
def request_albums(request, id):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(serializers.serialize("json", Album.objects.filter(owner_id = id)))
    return response

@csrf_exempt
def create_album(request):
    if request.method == 'POST':
        album = createAlbum(request.user.id ,request.POST['album_name'],request.POST['album_description'])
        return HttpResponseRedirect(reverse('album_detail', kwargs={'slug': album.slug}))

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        # Name, Content, AlbumID, Isorginal = True, Intro = ""
        name = request.FILES['files[]'].name
        content = ContentFile(request.FILES['files[]'].read())
        album_name = request.POST['selector']
        albumId = getAlbumIdByName(request.user.id, album_name)
        intro = request.POST['photo_description']
        photo = createPhoto(Name=name, Content=content, AlbumID=albumId, Intro=intro)
        return HttpResponseRedirect(reverse('photo_detail', kwargs={'slug': photo.slug}))

class AboutView(TemplateView):
    template_name = "about.html"