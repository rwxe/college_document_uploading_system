import django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.utils import DataError
from django.urls import reverse
from django.contrib.auth import hashers
from django.core import mail, cache
from django.db.models import Q
from . import models
import random
import string
import datetime
import random
from django.conf import settings
import sys

# Create your views here.
def hint_and_redirect(request, the_url, hint, show_hint=True, delay_time=1000):
    if show_hint == False:
        return redirect(the_url)
    else:
        context = {'the_url': the_url,
                   'hint': hint,
                   'delay_time': delay_time,
                   }
        return render(request, 'cdus/hint.html', context)

def index(request):
    context={}
    return render(request, 'cdus/index.html', context)

def qft(request):
    return HttpResponse("快速功能测试")


def login(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'cdus/login.html', context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        p1 = request.POST.get('password1')

        try:
            result = models.Teacher.objects.get(email=email)
            if hashers.check_password(p1, result.password):
                request.session['name'] = result.name
                request.session['id'] = result.id
                # 登录成功
               # context = {'the_url': reverse('cdus:index'),
               #           'hint': '登录成功了',
               #           'page': '主页',
               #           }
               # return render(request, 'cdus/hint.html', context)
                return hint_and_redirect(request, reverse('cdus:index'), '登录成功了', False)

            else:
                context = {'err_msg': '密码错误',
                           }
                return render(request, 'cdus/login.html', context)

        except models.Teacher.DoesNotExist:
            context = {'err_msg': '此用户不存在',
                       }
            return render(request, 'cdus/login.html', context)
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()
            print(sys.exc_info())
            return HttpResponse("出BUG了")
    else:
        return HttpResponse("出BUG了")


def register(request):
    # 注册页面
    if request.method == 'GET':
        # 是否发送了验证码
        request.session['sent'] = 'no'
        context = {'err_msg': '',
                   'sent': 'no',
                   }
        return render(request, 'cdus/register.html', context)
    elif request.method == 'POST':
        # print("会话项目",request.session.items())
        # print("会话过期秒数",request.session.get_expiry_age())
        # print("会话到期时间",request.session.get_expiry_date())
        name = request.POST.get('name')
        email = request.POST.get('email')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        if request.session.get('sent') == 'no':
            # 这里由于偷懒，并没有记录是否发送成功了
            try:
                send_verify_code(request, email)
            except Exception as e:
                print(e)
                print(sys.exc_info())
                request.session['sent'] = 'no'
                context = {'err_msg': '验证码的发送出现了问题，这可能在短时间内无法解决，请改日再来',
                           'sent': 'no',
                           }
                return render(request, 'cdus/register.html', context)

            context = {'name': name,
                       'email': email,
                       'password1': p1,
                       'password2': p2,
                       'sent': 'yes'
                       }
            request.session['sent'] = 'yes'
            return render(request, 'cdus/register.html', context)
        if request.session.get('sent') == 'yes':
            if request.session.get('verify_code') != request.POST.get('verify_code'):
                context = {'err_msg': '验证码输入错误',
                           'name': name,
                           'email': email,
                           'password1': p1,
                           'password2': p2,
                           'sent': 'yes',
                           }
                return render(request, 'cdus/register.html', context)
        if request.session.get('sent') == None:
            context = {'err_msg': '验证码过期，请重新获取',
                       'sent': 'no',
                       }
            return render(request, 'cdus/register.html', context)

        new_user = models.User()
        name = request.POST.get('name')
        # 邮箱也要检测是否唯一
        email = request.POST.get('email')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')

        try:
            # 检测数据库中是否已存在同名用户，若抛出该用户
            # 名不存在异常，则为可以存入数据库
            models.User.objects.get(name=name)
            context = {'err_msg': '此用户名已存在，请更换一个',
                       }
            return render(request, 'cdus/register.html', context)
        except models.User.DoesNotExist:
            new_user.name = name

        try:
            # 检测数据库中是否已存在相同邮箱，若抛出该邮箱
            # 不存在异常，则为可以存入数据库
            models.User.objects.get(email=email)
            context = {'err_msg': '此邮箱已存在，请更换一个',
                       }
            return render(request, 'cdus/register.html', context)
        except models.User.DoesNotExist:
            new_user.email = email

        if p1 != p2:
            context = {'err_msg': '两次输入的密码不同，请检查是否有误',
                       }
            return render(request, 'cdus/register.html', context)
        else:
            p1_encrypted = hashers.make_password(p1, None, 'pbkdf2_sha256')
            new_user.password = p1_encrypted
            try:
                new_user.save()
                # 注册成功
               # context = {'the_url': reverse('cdus:index'),
               #           'hint': '注册成功了',
               #           'page': '主页',
               #           }
               # return render(request, 'cdus/hint.html', context)
                return hint_and_redirect(request, reverse('cdus:index'), '注册成功了')

            except DataError:
                context = {'err_msg': '数据错误，请检查您输入的内容是否符合格式',
                           }
                return render(request, 'cdus/register.html', context)
            except:
                return HttpResponse("出BUG了")
