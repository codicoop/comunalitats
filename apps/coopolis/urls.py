#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .admin import coopolis_admin_site
from .views import CoopolisCoursesListView, ProjectFormView, SignUp, LogIn
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView


urlpatterns = [
    url('admin/login', RedirectView.as_view(pattern_name=settings.LOGIN_URL, permanent=True, query_string=True)),
]

urlpatterns += [
    path('login/', LogIn.CoopolisLoginView.as_view(), name='login'),
    path('users/login/', LogIn.CoopolisLoginView.as_view(), name='login'),
    path('signup', SignUp.signup, name='signup'),
    path('admin/', coopolis_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', CoopolisCoursesListView.as_view(), name='home'),
    path('project/', ProjectFormView.as_view(), name='project'),
]
