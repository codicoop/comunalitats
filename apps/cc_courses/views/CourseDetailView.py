#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class CourseDetailView(generic.DetailView):
    model = apps.get_model('cc_courses', 'Course')
    template_name = 'course.html'

