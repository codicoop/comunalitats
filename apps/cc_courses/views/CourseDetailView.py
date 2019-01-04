#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from cc_courses.models import Course


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course.html'

