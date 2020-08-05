#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import reverse
from constance import config
from django.conf import settings
from django.template import Template, Context
from django.core.mail.message import EmailMultiAlternatives
from django.utils.html import strip_tags

from cc_courses.models import Activity, ActivityEnrolled
from coopolis_backoffice.custom_mail_manager import MyMailTemplate


class EnrollActivityView(generic.RedirectView):

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.POST:
            self.url = reverse('loginsignup')
        else:
            activity = Activity.objects.get(id=request.POST['activity_id'])
            enrollment = ActivityEnrolled(
                user=request.user,
                activity=activity,
                user_comments=request.POST['user_comments'],
            )
            self.url = activity.course.absolute_url
            enrollment.save()
            if enrollment.waiting_list:
                enrollment.send_waiting_list_email()
            else:
                enrollment.send_confirmation_email()

        return super().get(request, *args, **kwargs)
