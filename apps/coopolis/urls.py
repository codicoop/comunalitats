#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .admin import coopolis_admin_site
import apps.cc_courses.views as views
from apps.coopolis.views.ProjectFormView import ProjectFormView

urlpatterns = [
    path('admin/', coopolis_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', views.CoursesListView.as_view(), name='home'),
    path('project/<pk>', ProjectFormView.as_view(), name='project')
]
