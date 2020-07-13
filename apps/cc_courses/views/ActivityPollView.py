#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from cc_courses.models import Activity


class ActivityPollView(DetailView):
    model = Activity
    template_name = 'poll.html'
