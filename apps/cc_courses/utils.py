#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from .views import CoursesListView
from importlib import import_module


def get_courses_list_view_class():
    if hasattr(settings, 'COURSES_LIST_VIEW_CLASS'):
        values = settings.COURSES_LIST_VIEW_CLASS.split('.')
        module = import_module('.'.join(values[:-1]))
        cl = getattr(module, values[-1])
        return cl
    return CoursesListView
