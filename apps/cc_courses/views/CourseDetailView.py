#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from cc_courses.models import Course, Activity


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.all()[:5]
        # context['past_courses'] = Course.objects.filter(date_end__lt=timezone.now().date())
        return context

