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


def login(request,user_type):
    # 转换成小写，确保下面比对不会出问题
    user_type=user_type.lower()

    if request.method == 'GET':
        context = {}
        return render(request, 'cdus/login.html', context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        p1 = request.POST.get('password1')

        try:
            # 判别用户类型
            if user_type=='teacher':
                result = models.Teacher.objects.get(email=email)
            elif user_type=='approver':
                result = models.Approver.objects.get(email=email)
            else:
                print("BUG,不知道这是什么用户类型")
                return HttpResponse("我不知道这是什么用户类型")

            if hashers.check_password(p1, result.password):
                request.session['name'] = result.name
                request.session['id'] = result.id
                request.session['user_type'] = user_type
                return hint_and_redirect(request, reverse('cdus:index'), '登录成功了', False)

            else:
                context = {'err_msg': '密码错误',
                           }
                return render(request, 'cdus/login.html', context)

        except models.Teacher.DoesNotExist:
            context = {'err_msg': '此用户不存在',
                       }
            return render(request, 'cdus/login.html', context)
        except models.Approver.DoesNotExist:
            context = {'err_msg': '此用户不存在',
                       }
            return render(request, 'cdus/login.html', context)
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()
            print(sys.exc_info())
            return HttpResponse("出BUG了")
    else:
        return HttpResponse("出BUG了")


def register(request,user_type):
    # 注册页面
    if request.method == 'GET':
        colleges=models.College.objects.all()
        if user_type=='teacher':
            the_type='教师'
        elif user_type=='approver':
            the_type='审批人'
        else:
            the_type='未知用户类型'

        context = {'err_msg': '',
                'colleges':colleges,
                'user_type':the_type
                   }
        return render(request, 'cdus/register.html', context)
    elif request.method == 'POST':


        name = request.POST.get('name')
        # 邮箱也要检测是否唯一
        email = request.POST.get('email')
        college_id =request.POST.get('college')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')

        if user_type=='teacher':
            new_user = models.Teacher()
            new_user.college=models.College.objects.get(pk=college_id)
            TYPE_USER=models.Teacher
        elif user_type=='approver':
            new_user = models.Approver()
            new_user.college=models.College.objects.get(pk=college_id)
            TYPE_USER=models.Approver
        else:
            print("BUG,不知道这是什么用户类型")
            return HttpResponse("我不知道这是什么用户类型")

        try:
            # 检测数据库中是否已存在同名用户，若抛出该用户
            # 名不存在异常，则为可以存入数据库

            TYPE_USER.objects.get(name=name)
            context = {'err_msg': '此用户名已存在，请更换一个',
                       }
            return render(request, 'cdus/register.html', context)
        except TYPE_USER.DoesNotExist:
            new_user.name = name

        try:
            # 检测数据库中是否已存在相同邮箱，若抛出该邮箱
            # 不存在异常，则为可以存入数据库
            TYPE_USER.objects.get(email=email)
            context = {'err_msg': '此邮箱已存在，请更换一个',
                       }
            return render(request, 'cdus/register.html', context)
        except TYPE_USER.DoesNotExist:
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
                return hint_and_redirect(request, reverse('cdus:index'), '注册成功了')

            except DataError:
                context = {'err_msg': '数据错误，请检查您输入的内容是否符合格式',
                           }
                return render(request, 'cdus/register.html', context)
            except:
                ex_type, ex_val, ex_stack = sys.exc_info()
                print(sys.exc_info())
                return HttpResponse("出BUG了")
