#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .admin import coopolis_admin_site
from cc_courses.views import CoursesListView
from .views import ProjectFormView

urlpatterns = [
    path('admin/', coopolis_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', CoursesListView.as_view(), name='home'),
    path('project/<id>', ProjectFormView.as_view(), name='project')
]
