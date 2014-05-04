#-*- coding: utf-8 -*-
import re
import urllib
from datetime import datetime
from django.shortcuts import render_to_response

# Create your views here.

def getImg(url, imgType):
	page = urllib.urlopen(url)
	html = page.read()
	# reg = r'src="(.*?\.+'+imgType+'!slider)"' #这个正则表达式是最关键的，取得图片链接就靠它了
	reg = r'src=".*?\.'+imgType+'"'
	print reg
	imgre = re.compile(reg)
	imgList = re.findall(imgre, html)
	prefix = '/home/michael/Pictures/' # 图片保存路径前缀
	x = 0
	for imgurl in imgList:
		print imgurl
		urllib.urlretrieve(imgurl, '%s%s.%s' %(prefix, datetime.now(), imgType)) #urlretrieve下载图片到本地
		x += 1
	return imgList

def issue(request):
	query = request.GET.get('q','')
	if query:
		imglist = getImg(query, 'jpg')
	else:
		imglist = []
	return render_to_response('crawler.html', {'query': query, 'results': imglist})