# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^seluser$', views.seluser),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quote$', views.quote),
    url(r'^fav$', views.fav),
    url(r'^removefav$', views.removefav),
    url(r'^deleteuser$', views.deleteuser),
    url(r'^logout$', views.logout),
    ]