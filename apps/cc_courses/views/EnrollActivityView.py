#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import reverse
from cc_courses.models import Activity


class EnrollActivityView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('login')
        else:
            activity = Activity.objects.get(id=kwargs['id'])
            request.user.enrolled_activities.add(activity)
            self.url = activity.course.absolute_url
        return super().get(request, *args, **kwargs)
