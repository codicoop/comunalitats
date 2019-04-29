#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import reverse
from cc_courses.models import Activity
from constance import config
from django.core.mail import send_mail
from coopolis_backoffice import settings


class EnrollActivityView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('loginsignup')
        else:
            activity = Activity.objects.get(id=kwargs['id'])
            request.user.enrolled_activities.add(activity)
            self.url = activity.course.absolute_url
            # self._send_confirmation_email(activity)
        return super().get(request, *args, **kwargs)

    def _send_confirmation_email(self, activity):
        mail_to = {self.request.user.email}
        if settings.DEBUG:
            mail_to.add(config.EMAIL_TO_DEBUG)
        message = config.EMAIL_ENROLLMENT_CONFIRMATION.format(
            activity.name,
            activity.date_start,
            activity.starting_time,
            activity.ending_time,
            activity.place,
            reverse('my_activities'),
            config.CONTACT_EMAIL,
            config.CONTACT_PHONE_NUMBER
        )
        send_mail(
            subject=config.EMAIL_ENROLLMENT_CONFIRMATION_SUBJECT.format(activity.name),
            message=message,
            html_message=message,
            recipient_list=mail_to,
            from_email=config.EMAIL_FROM
        )
