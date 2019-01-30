#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.urls import include
from apps.cc_users import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('users/signup', views.signup, name='signup'),
    path('users/activate/<uuid>/<token>/', views.activate, name='users_activate'),
    path('users/login/', views.UsersLoginView.as_view(), name='login'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/profile/', login_required(views.MyAccountView), name='user_profile'),
]
