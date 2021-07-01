# -*-coding:utf-8-*-
from django.urls import path

from . import views

app_name= 'cdus'
urlpatterns = [
        path('',views.index,name='index'),
        path('qft',views.qft,name='qft'),
        path('login',views.login,name='login'),
        path('register',views.register,name='register'),
        ]
