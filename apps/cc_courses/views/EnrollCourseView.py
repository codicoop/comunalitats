#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import reverse
from cc_courses.models import Course


class EnrollCourseView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('login')
        else:
            course = Course.objects.get(slug=kwargs['slug'])
            request.user.enrolled_courses.add(course)
            self.url = request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)
