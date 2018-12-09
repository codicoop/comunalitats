#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from cc_courses.models import Course
from django.utils import timezone


class CoursesListView(generic.ListView):
    model = Course
    template_name = 'courses.html'
    queryset = Course.objects.filter(date_end__gte=timezone.now().date())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_courses'] = context['course_list']
        context['past_courses'] = Course.objects.filter(date_end__lt=timezone.now().date())
        return context
