#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from .views import CoursesListView
from importlib import import_module


def get_courses_list_view_class():
    if hasattr(settings, 'COURSES_LIST_VIEW_CLASS'):
        module = import_module(settings.COURSES_VIEWS)
        cl = getattr(module, settings.COURSES_LIST_VIEW_CLASS)
        return cl
    return CoursesListView
