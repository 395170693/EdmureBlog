from django import forms
from django.forms import widgets
from django.forms import fields
from . import models
from django.core.exceptions import ValidationError

from django.forms import fields as django_fields
from django import forms as django_forms
class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseForm, self).__init__(*args, **kwargs)

class RegisterForm(forms.Form):
    username = fields.CharField(
            error_messages={"required": "用户名不能为空"},
            widget=widgets.Input(attrs={"class": "form-control"})
    )
    email = fields.EmailField(
           error_messages={'required':'邮箱不能为空','invalid':'邮箱格式错误'},
            widget=widgets.Input(attrs={"class": "form-control"})
    )
    password = fields.CharField(
            max_length=12,
            min_length=6,
            error_messages={"required": "密码不能为空",'invalid':'密码应大于6位小于12位！'},
            widget=widgets.Input(attrs={"class": "form-control"})
    )
    password2 = fields.CharField(error_messages={"required": "密码不能为空"},
                                 widget=widgets.Input(attrs={"class": "form-control"}))
    check_code = fields.CharField(error_messages={"required": "验证码不能为空"},
                                  widget=widgets.Input(attrs={"class": "form-control"}))

    def clean_username(self):
        """
        验证用户存不存在
        :return:
        """
        obj = models.UserInfo.objects.filter(username=self.cleaned_data['username'])
        # 用户存在返回原来的值
        if not obj:
            return self.cleaned_data['username']
        else:
            raise ValidationError(message="用户已存在，请更换其他用户名", code="xxxx")

class LoginForm(BaseForm, django_forms.Form):
    username = django_fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"}
    )
    password = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    rmb = django_fields.IntegerField(required=False)

    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')
