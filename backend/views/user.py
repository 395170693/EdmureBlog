#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from repository import models

def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        username = request.session.get('username')
        email = request.session.get('email')
        #print('2222222222222222222222222222222222222222')
        return render(request, 'backend_base_info.html',{'username':username,'email':email})
    if request.method == 'POST':
        print("111111111111111111111111111111111111111111111111111")
        nickname = request.POST.get('nickname')
        blogUrl = request.POST.get('blogUrl')
        blogTheme = request.POST.get('blogTheme')
        blogTitle = request.POST.get('blogTitle')
        data = models.UserInfo.objects.filter(username=request.session.get('username'))
        data.update(nickname=nickname)
        # data.fans
def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    return render(request, 'backend_tag.html')


def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    return render(request, 'backend_category.html')


def article(request):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    return render(request, 'backend_article.html')


def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    return render(request, 'backend_add_article.html')


def edit_article(request):
    """
    编辑文章
    :param request:
    :return:
    """
    return render(request, 'backend_edit_article.html')