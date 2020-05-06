#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from cc_courses.models import Activity, ActivityEnrolled
from django.utils import timezone


class MyCoursesListView(generic.ListView):
    model = Activity
    template_name = 'my_courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled_activities'] = ActivityEnrolled.objects.filter(
            activity__date_start__gte=timezone.now().date(), user=self.request.user, waiting_list=False)
        context['waiting_list_activities'] = ActivityEnrolled.objects.filter(
            activity__date_start__gte=timezone.now().date(), user=self.request.user, waiting_list=True)
        context['past_enrolled_activities'] = ActivityEnrolled.objects.filter(
            activity__date_start__lt=timezone.now().date(), user=self.request.user)
        return context
