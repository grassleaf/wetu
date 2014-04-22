#coding: utf-8
import datetime
from django.core.context_processors import csrf
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import Context, loader
from data.models import *
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from blog.models import Post, Category, Widget
from wetu.settings import PAGE_NUM, RECENTLY_NUM

import logging
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
def create_album(request):
    if request.method == 'POST':
        createAlbum(request.user.id ,request.POST['album_name'],request.POST['album_description'])
        return redirect('/')
    else:
        return render_to_response('create_album.html')

@csrf_exempt
def upload(request):

    import uuid

    # settings for the file upload
    #   you can define other parameters here
    #   and check validity late in the code
    options = {
        # the maximum file size (must be in bytes)
        "maxfilesize": 2 * 2 ** 20, # 2 Mb
        # the minimum file size (must be in bytes)
        "minfilesize": 1 * 2 ** 10, # 1 Kb
        # the file types which are going to be allowed for upload
        #   must be a mimetype
        "acceptedformats": (
            "image/jpeg",
            "image/png",
        )
    }
    if request.method == 'POST':
        print request.POST
        return render_to_response('upload.html')
    else: #GET
        # load the template
        t = loader.get_template("upload.html")
        c = Context({
            # the unique id which will be used to get the folder path
            # "uid": uuid.uuid4(),
            "albums": Album.objects.all(),
            # these two are necessary to generate the jQuery templates
            # they have to be included here since they conflict with django template system
            "open_tv": u'{{',
            "close_tv": u'}}',
            # some of the parameters to be checked by javascript
            "maxfilesize": options["maxfilesize"],
            "minfilesize": options["minfilesize"],
            })
        # add csrf token value to the dictionary
        c.update(csrf(request))
        # return
        return HttpResponse(t.render(c))

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['categories'] = Category.available_list()
            context['widgets'] = Widget.available_list()
            context['recently_posts'] = Post.get_recently_posts(RECENTLY_NUM)
        except Exception as e:
            print '加载基本信息出错'
            logger.exception(u'加载基本信息出错[%s]！', e)

        return context

class IndexView(BaseMixin, ListView):
    query = None
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        try:
            self.cur_page = int(request.GET.get('page', 1))
        except TypeError:
            self.cur_page = 1

        if self.cur_page < 1:
            self.cur_page = 1

        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.object_list, PAGE_NUM)
        kwargs['posts'] = paginator.page(self.cur_page)
        kwargs['query'] = self.query
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.query = self.request.GET.get('s')
        if self.query:
            qset = (
                Q(title__icontains=self.query) |
                Q(content__icontains=self.query)
            )
            # posts = Post.objects.defer('content_rst', 'content_html')\
            #     .filter(qset, status=0)
            posts = Post.objects.defer('content', ).filter(qset, status=0)
            for post in posts:
                post.title = post.title.replace(self.query, '<span class="hightline">%s</span>' % self.query)
                post.summary = post.summary.replace(self.query, '<span class="hightline">%s</span>' % self.query)
        else:
            posts = Post.objects.defer('content', ).filter(status=0)
        return posts

class CategoryListView(IndexView):
    def get_queryset(self):
        # alias = self.kwargs.get('alias')
        slug = self.kwargs.get('slug')

        try:
            self.category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return []

        # posts = self.category.post_set.defer('content_rst', 'content_html').filter(status=0)
        posts = self.category.post_set.defer('content', ).filter(status=0)
        return posts

    def get_context_data(self, **kwargs):
        if hasattr(self, 'category'):
            kwargs['title'] = self.category.name + ' | '

        return super(CategoryListView, self).get_context_data(**kwargs)

class PostDetailView(BaseMixin, DetailView):
    """docstring for PostDetailView"""

    object = None
    template_name = 'post_detail.html'
    queryset = Post.objects.filter(status=0)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        post = self.queryset.get(slug=slug)
        return super(PostDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = self.get_object()
        next_id = post.id + 1
        prev_id = post.id - 1

        try:
            next_post = self.queryset.get(id=next_id)
        except Post.DoesNotExist:
            next_post = None

        try:
            prev_post = self.queryset.get(id=prev_id)
        except Post.DoesNotExist:
            prev_post = None

        context['next_post'] = next_post
        context['prev_post'] = prev_post

        # context['lru_views'] = cache.get('lru_views', {}).items()
        # context['cur_user_ip'] = self.cur_user_ip

        # context['related_posts'] = post.related_posts

        return context