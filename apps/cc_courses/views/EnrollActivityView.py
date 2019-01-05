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
            course = Activity.objects.get(id=kwargs['id'])
            request.user.enrolled_activities.add(course)
            self.url = request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)
