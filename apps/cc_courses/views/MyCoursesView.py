#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from cc_courses.models import Course
from django.utils import timezone


class MyCoursesListView(generic.ListView):
    model = Course
    template_name = 'my_courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_courses'] = self.request.user.enrolled_courses.filter(date_end__gte=timezone.now().date())
        context['past_courses'] = self.request.user.enrolled_courses.filter(date_end__lt=timezone.now().date())
        return context
