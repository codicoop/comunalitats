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
                self._send_waiting_list_email(activity)
            else:
                self._send_confirmation_email(activity)

        return super().get(request, *args, **kwargs)

    def _send_confirmation_email(self, activity):
        mail = MyMailTemplate('EMAIL_ENROLLMENT_CONFIRMATION')
        mail.to = self.request.user.email
        mail.subject_strings = {
            'activitat_nom': activity.name
        }
        mail.body_strings = {
            'activitat_nom': activity.name,
            'ateneu_nom': config.PROJECT_FULL_NAME,
            'activitat_data_inici': activity.date_start.strftime("%d-%m-%Y"),
            'activitat_hora_inici': activity.starting_time.strftime("%H:%M"),
            'activitat_lloc': activity.place,
            'absolute_url_my_activities': f"{settings.ABSOLUTE_URL}{reverse('my_activities')}",
            'url_web_ateneu': config.PROJECT_WEBSITE_URL,
        }
        mail.send()

    def _send_waiting_list_email(self, activity):
        mail = MyMailTemplate('EMAIL_ENROLLMENT_WAITING_LIST')
        mail.to = self.request.user.email
        mail.subject_strings = {
            'activitat_nom': activity.name
        }
        mail.body_strings = {
            'activitat_nom': activity.name,
            'ateneu_nom': config.PROJECT_FULL_NAME,
            'activitat_data_inici': activity.date_start.strftime("%d-%m-%Y"),
            'activitat_hora_inici': activity.starting_time.strftime("%H:%M"),
            'activitat_lloc': activity.place,
            'url_els_meus_cursos': f"{settings.ABSOLUTE_URL}{reverse('my_activities')}",
            'url_ateneu': settings.ABSOLUTE_URL,
        }
        mail.send()
