#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from cc_courses.models import Activity
from django.utils import timezone


class MyCoursesListView(generic.ListView):
    model = Activity
    template_name = 'my_courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled_activities'] = Activity.objects.filter(date_start__gte=timezone.now().date(),
                                                                 enrolled=self.request.user)
        context['past_enrolled_activities'] = Activity.objects.filter(date_start__lt=timezone.now().date(),
                                                                      enrolled=self.request.user)
        return context
