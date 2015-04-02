#!/usr/bin/python
#coding=utf-8
from django.conf.urls import patterns, include, url
from BBS import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.Index,name='index'),
    url(r'^detail/(\d+)/$',views.Detail,name='detail'),
    url(r'^login/$',views.Login,name='login'),
    url(r'^logout/$',views.LoginOut,name='logout'),
    url(r'^write/$',views.InsertContent,name='write'),
    url(r'^show/$',views.ShowList,name='show'),
    url(r'^veri/$',views.verify_code,name='验证码'),
    url(r'^about/$',views.About,name='关于'),
    url(r'^register/$',views.Register,name='注册'),
)
