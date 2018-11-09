#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .admin import coopolis_admin_site

urlpatterns = [
    path('admin/', coopolis_admin_site.urls),
]
