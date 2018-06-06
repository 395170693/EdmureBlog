#!/usr/bin/env python
# -*- coding:utf-8 -*-
from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import render
from utils.check_code import create_validate_code
import json
from repository import forms
from repository import models
from repository.forms import LoginForm

def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        print('11111111111111111111111111111111111')
        return render(request, 'login.html')
        #pass
    elif request.method == 'POST':
        print('22222222222222222222222222222222222222')
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('nid', 'nickname',
                       'username', 'email',
                       'avatar',
                       'blog__nid',
                       'blog__site').first()

            if not user_info:
                # result['message'] = {'__all__': '用户名或密码错误'}
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            print(form.errors)
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))

    # if request.method == "POST":
    #     if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
    #         pass
    #     else:
    #         print('验证码错误')
    #
    #
    # return render(request, 'login.html')



def register(request):
    """
    注册
    :param request:
    :return:
    """
    ret = {"status":False,'error':None,'data':None}
    if request.method == 'GET':
        register_obj = forms.RegisterForm()
        return render(request,'register.html',{'register_obj':register_obj})
    elif request.method == "POST":
        register_obj = forms.RegisterForm(request.POST)
        if register_obj.is_valid():
            ret["status"] = True
            ret['data'] = register_obj.cleaned_data
            request.session['username'] = request.POST.get('username')
            request.session['email'] = request.POST.get('email')
            models.UserInfo.objects.create(username=request.POST.get('username'),
                                           email=request.POST.get('email'),
                                           password=request.POST.get('email')
                                           )
        else:
            ret['error'] = register_obj.errors.as_json()
            request.session.clear()
        request.session.set_expiry(60 * 60 * 24 * 7)
        result = json.dumps(ret)
        # 不能使用render，使用render返回数据,前端var data1=JSON.parse(arg)转换报错。可以使用HttpResponse直接返回数据
        # return render(request, 'register.html',{"result":result})
        return HttpResponse(result)

# def register(request):
#     """
#     注册
#     :param request:
#     :return:
#     """
#     ret = {"status": False, "error": None, "data": None}
#     if request.method == "GET":
#         register_obj = forms.RegisterForm()
#         return render(request, 'register.html', {"register_obj": register_obj})
#     elif request.method == "POST":
#         register_obj = forms.RegisterForm(request.POST)
#         if register_obj.is_valid():
#             ret["status"] = True
#             ret["data"] = register_obj.cleaned_data
#         else:
#             ret["error"] = register_obj.errors.as_data()
#         result = json.dumps(ret, cls=JsonCunstomEncode)
#         # 不能使用render，使用render返回数据,前端var data1=JSON.parse(arg)转换报错。可以使用HttpResponse直接返回数据
#         # return render(request, 'register.html',{"result":result})
#         return HttpResponse(result)
#     # return render(request, 'register.html')


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    pass


from django.core.exceptions import ValidationError
class JsonCunstomEncode(json.JSONEncoder):
    def default(self, field):
        if isinstance(field,ValidationError):
            return {"code":field.code,"message":field.message}
        else:
            return json.JSONEncoder.default(self,field)

