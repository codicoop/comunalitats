#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import reverse
from constance import config
from django.conf import settings
from django.template import Template, Context

from cc_courses.models import Activity, ActivityEnrolled


class EnrollActivityView(generic.RedirectView):

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.POST:
            self.url = reverse('loginsignup')
        else:
            activity = Activity.objects.get(id=request.POST['activity_id'])
            is_full = activity.remaining_spots < 1
            enrollment = ActivityEnrolled(
                user=request.user,
                activity=activity,
                user_comments=request.POST['user_comments'],
                waiting_list=True if is_full else False
            )
            self.url = activity.course.absolute_url
            enrollment.save()
            if is_full:
                self._send_waiting_list_email(activity)
            else:
                self._send_confirmation_email(activity)

        return super().get(request, *args, **kwargs)

    def _send_confirmation_email(self, activity):
        from django.core.mail.message import EmailMultiAlternatives
        from django.utils.html import strip_tags

        context = Context({
            'activity': activity,
            'absolute_url': self.request.build_absolute_uri(reverse('my_activities')),
            'contact_email': config.CONTACT_EMAIL,
            'contact_number': config.CONTACT_PHONE_NUMBER,
            'request': self.request,
        })
        template = Template(config.EMAIL_ENROLLMENT_CONFIRMATION)
        html_content = template.render(context)  # render with dynamic value
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

    def _send_waiting_list_email(self, activity):
        from django.core.mail.message import EmailMultiAlternatives
        from django.utils.html import strip_tags

        context = Context({
            'activity': activity,
            'absolute_url': self.request.build_absolute_uri(reverse('my_activities')),
            'contact_email': config.CONTACT_EMAIL,
            'contact_number': config.CONTACT_PHONE_NUMBER,
            'request': self.request,
        })
        template = Template(config.EMAIL_ENROLLMENT_WAITING_LIST)
        html_content = template.render(context)  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        mail_to = {self.request.user.email}
        if settings.DEBUG:
            mail_to.add(config.EMAIL_TO_DEBUG)

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(
            config.EMAIL_ENROLLMENT_WAITING_LIST_SUBJECT.format(activity.name),
            text_content,
            config.EMAIL_FROM_ENROLLMENTS,
            mail_to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
