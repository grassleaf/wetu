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
from data.func import createInfo

# Create your views here.

# def index(request):
#     username = request.session.get('username', None)
#     return render_to_response('index.html', {'username': username})

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        # 该用户是否存在
        if not _validate_email(email):
            error = '邮箱已被占用'
        elif not _validate_username(username):
            error = '昵称已被占用'
        else:
            # user = User.objects.create_user(username,email,password)
            # user.save()
            createInfo(username, password, email)
            # 发送邮件
            # user.email_user("欢迎你注册", "http://blabla")
            _login(request, username, password) #注册后直接登陆
            return redirect("/", {'username': username}) # 返回登录前的页面
        return render_to_response("register.html", {'error': error})
    else:
        return render_to_response("register.html")

def _validate_username(username):
    users = User.objects.filter(username=username)
    return True if not users else False # 模拟三操作符

def _validate_email(email):
    emails = User.objects.filter(email=email)
    return True if not emails else False

def _login(request, username, password):
    ret = False
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            request.session['username'] = username
            ret = True
        else:
            # messages.add_message(request, messages.INFO, _(u'用户没有激活'))
            print '用户没有激活'
    else:
        # messages.add_message(request, messages.INFO, _(u'用户不存在'))
        print '用户不存在'
    return ret

@csrf_exempt
def login(request):
    c = {}
    c.update(csrf(request))
    if not (request.method == 'POST'):
        # 记住登录前的url，如果没有则设置为登录页('/login')
        # request.session['login_from'] = request.META.get('HTTP_REFERER', '/login')
        return render_to_response('login.html')
    username = request.POST['username'] #用户可能输入email
    password = request.POST['password']
    if _login(request, username, password):
        print username, 'logined at ', datetime.datetime.now()
        return redirect("/")
        # return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect('.')

@csrf_exempt
def logout(request):
    print request.user.get_username(), 'logouted at ', datetime.datetime.now()
    auth.logout(request)
    request.session['username'] = None
    # url = request.session['login_from']
    request.session['login_from'] = None
    return HttpResponseRedirect('/')

# def validate_input(request):
#     response = HttpResponse()
#     response['Content-Type'] = "text/javascript"
#     array = {
#         'valid' : false,
#         'message' : 'Post argument "user" is missing.'
#     }
#     response.write(serializers.serialize("json", array))
#     return response