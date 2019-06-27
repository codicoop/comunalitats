#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import reverse
from cc_courses.models import Activity
from constance import config
from django.core.mail import send_mail
from django.conf import settings


class EnrollActivityView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('loginsignup')
        else:
            activity = Activity.objects.get(id=kwargs['id'])
            request.user.enrolled_activities.add(activity)
            self.url = activity.course.absolute_url
            self._send_confirmation_email(activity)
        return super().get(request, *args, **kwargs)

    def _send_confirmation_email(self, activity):
        from django.core.mail.message import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags

        context = {
            'activity': activity,
            'absolute_url': self.request.build_absolute_uri(reverse('my_activities')),
            'contact_email': config.CONTACT_EMAIL,
            'contact_number': config.CONTACT_PHONE_NUMBER
        }
        html_content = render_to_string('emails/base.html', context)  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        mail_to = {self.request.user.email}
        if settings.DEBUG:
            mail_to.add(config.EMAIL_TO_DEBUG)

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(
            config.EMAIL_ENROLLMENT_CONFIRMATION_SUBJECT.format(activity.name),
            text_content,
            config.EMAIL_FROM_ENROLLMENTS,
            mail_to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
