#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.urls import include
from apps.cc_users import views

urlpatterns = [
    path('login/', views.UsersLoginView.as_view(), name='login'),
    path('signup', views.signup, name='signup'),
    path('activate/<uuid>/<token>/', views.activate, name='users_activate'),
    path('users/', include('django.contrib.auth.urls')),
]
