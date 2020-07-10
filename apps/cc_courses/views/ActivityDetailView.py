#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from cc_courses.models import Activity


class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['something'] = "lala"
        return context
