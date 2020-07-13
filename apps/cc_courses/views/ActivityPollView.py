#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from cc_courses.models import Activity


class ActivityPollView(DetailView):
    model = Activity
    template_name = 'poll.html'

    def get(self, request, *args, **kwargs):
        ret = super(ActivityPollView, self).get(request, *args, **kwargs)
        if not self.object.poll_access_allowed():
            return HttpResponseRedirect(reverse('my_activities'))
        return super(ActivityPollView, self).get(request, *args, **kwargs)
