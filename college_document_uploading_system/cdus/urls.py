# -*-coding:utf-8-*-
from django.urls import path

from . import views

app_name= 'cdus'
urlpatterns = [
        path('',views.index,name='index'),
        path('console/<str:user_type>',views.console,name='console'),
        path('post_doc/<str:ctc_id>',views.post_doc,name='post_doc'),
        path('qft',views.qft,name='qft'),
        path('login/<str:user_type>',views.login,name='login'),
        path('register/<str:user_type>',views.register,name='register'),
        ]
