# -*-coding:utf-8-*-
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name= 'cdus'
urlpatterns = [
        path('',views.index,name='index'),
        path('console/<str:user_type>',views.console,name='console'),
        path('post_doc/<int:ctc_id>',views.post_doc,name='post_doc'),
        path('review/<int:ud_id>/<str:op>',views.review,name='review'),
        path('qft',views.qft,name='qft'),
        path('login/<str:user_type>',views.login,name='login'),
        path('logout',views.logout,name='logout'),
        path('register/<str:user_type>',views.register,name='register'),
        ]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
