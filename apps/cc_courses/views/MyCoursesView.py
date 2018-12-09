#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from cc_courses.models import Activity
from django.utils import timezone


class MyCoursesListView(generic.ListView):
    model = Activity
    template_name = 'my_courses.html'

