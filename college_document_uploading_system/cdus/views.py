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

def register(request):
    pass

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
                request.session['username'] = result.username
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
            return HttpResponse("出BUG了")
    else:
        return HttpResponse("出BUG了")
    pass
