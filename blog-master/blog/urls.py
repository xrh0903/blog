# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from blogCMS import settings
from blog import views


urlpatterns = [
    url(r'^commentTree/(?P<article_id>\d+)/',views.commentTree),
    url(r'^up_count/',views.up_count),
    url(r'^down_count/',views.down_count),
    url(r'^(?P<username>.*)/backindex/$',views.backIndex),
    url(r'^(?P<username>.*)/backindex/addarticle/$',views.addarticle),
    url(r'^(?P<username>.*)/backindex/delarticle/$',views.delarticle),
    url(r'^(?P<username>.*)/backindex/editarticle/$',views.editarticle),
    url(r'^(?P<username>.*)/com', views.com),
    url(r'^(?P<username>.*)/(?P<condition>tag|category|date)/(?P<para>.*)', views.homeSite),
    url(r'^(?P<username>.*)/article/(?P<article_id>\d+)', views.homeSite),
    url(r'^(?P<username>.*)', views.homeSite,name="blog"),



]