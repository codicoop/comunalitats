#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from constance import config


class UserAdmin(admin.ModelAdmin):
    empty_value_display = '(cap)'
    list_display = ('first_name', 'last_name', 'id_number', 'email', 'project', 'enrolled_activities_count')
    search_fields = ('id_number', 'last_name', 'first_name', 'email', 'phone_number', 'cooperativism_knowledge')
    list_filter = ('gender', ('town', admin.RelatedOnlyFieldListFilter), 'residence_district', 'is_staff')
    fields = ['id', 'first_name', 'last_name', 'surname2', 'id_number', 'email', 'birthdate', 'birth_place',
              'town', 'residence_district', 'address', 'phone_number', 'educational_level',
              'employment_situation', 'discovered_us', 'cooperativism_knowledge', 'project', 'is_staff', 'groups',
              'is_active', 'date_joined', 'last_login']
    readonly_fields = ['id', 'last_login', 'date_joined', 'project']
    actions = ['copy_emails', ]

    def get_fields(self, request, obj=None):
        if request.user.is_superuser and "is_superuser" not in self.fields:
            self.fields.append('is_superuser')
        if obj is None and 'project' in self.fields:
            self.fields.remove('project')
            self.fields.remove('id')
            self.fields.remove('last_login')
        return super().get_fields(request, obj)

    def copy_emails(self, request, queryset):
        emails = []
        for user in queryset:
            emails.append(user.email)
        # self.message_user(request, "%s successfully marked as published." % message_bit)
        return HttpResponse(", ".join(emails))

    copy_emails.short_description = 'Copiar tots els e-mails'

    def save_model(self, request, obj, form, change):
        self.send_welcome_email(request.POST['email'])
        super().save_model(request, obj, form, change)

    def send_welcome_email(self, mail_to):
        mail_to = {mail_to}
        if settings.DEBUG:
            mail_to.add(config.EMAIL_TO_DEBUG)
        send_mail(
            subject=config.EMAIL_SIGNUP_WELCOME_SUBJECT,
            message=config.EMAIL_SIGNUP_WELCOME,
            html_message=config.EMAIL_SIGNUP_WELCOME,
            recipient_list=mail_to,
            from_email=settings.DEFAULT_FROM_EMAIL
        )
