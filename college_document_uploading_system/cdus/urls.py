# -*-coding:utf-8-*-
from django.urls import path

from . import views

app_name= 'cdus'
urlpatterns = [
        path('',views.index,name='index'),
        path('qft',views.qft,name='qft'),
        path('login/<str:user_type>',views.login,name='login'),
        path('register/<str:user_type>',views.register,name='register'),
        ]
