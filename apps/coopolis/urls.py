#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .admin import coopolis_admin_site
from .views import CoopolisCoursesListView, ProjectFormView

urlpatterns = [
    path('admin/', coopolis_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', CoopolisCoursesListView.as_view(), name='home'),
    path('project/<pk>', ProjectFormView.as_view(), name='project')
]
