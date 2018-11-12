#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from cc_courses.models import Course


class CoursesListView(generic.ListView):
    model = Course
    template_name = 'courses.html'
