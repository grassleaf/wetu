#coding: utf-8
from django.views.generic import TemplateView, DetailView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.files.base import ContentFile
from django.views.generic import DetailView

from data.models import Album, Photo
from data.func import *

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['albums'] = Album.objects.all()
        except Exception as e:
            print '加载基本信息出错'
            logger.exception(u'加载基本信息出错[%s]！', e)

        return context

class IndexView(BaseMixin, ListView):
    object = None
    user = None
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and (not request.user.is_superuser):
            self.user = request.user
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.user:
            info = getInfo(self.user.id)
            context['info'] = info[0]
        return context

    def get_queryset(self):
        return None

@csrf_exempt
def request_albums(request, id):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(serializers.serialize("json", Album.objects.filter(owner_id = id)))
    return response

@csrf_exempt
def create_album(request):
    if request.method == 'POST':
        album = createAlbum(request.user.id ,request.POST['albumname'],request.POST['albumdesc'])
        return HttpResponseRedirect(reverse('album_detail', kwargs={'slug': album.slug}))

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        # Name, Content, AlbumID, Isorginal = True, Intro = ""
        name = request.FILES['files[]'].name
        content = ContentFile(request.FILES['files[]'].read())
        album_name = request.POST['selector']
        albumId = getAlbumIdByName(request.user.id, album_name)
        intro = request.POST['photodesc']
        photo = createPhoto(Name=name, Content=content, AlbumID=albumId, Intro=intro)
        return HttpResponseRedirect(reverse('photo_detail', kwargs={'slug': photo.slug}))

class AboutView(TemplateView):
    template_name = "about.html"