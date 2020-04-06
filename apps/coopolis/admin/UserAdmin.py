#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from constance import config
from django.utils.safestring import mark_safe

from coopolis.forms import MySignUpAdminForm


class UserAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/grappellihacks.js',)
        css = {
            'all': ('styles/grappellihacks.css',)
        }

    form = MySignUpAdminForm
    empty_value_display = '(cap)'
    list_display = ('first_name', 'last_name', 'id_number', 'email', 'project', 'enrolled_activities_count')
    search_fields = ('id_number', 'last_name__unaccent', 'first_name__unaccent', 'email', 'phone_number',
                     'cooperativism_knowledge')
    list_filter = ('gender', ('town', admin.RelatedOnlyFieldListFilter), 'district', 'is_staff', 'fake_email',
                   'authorize_communications', )
    fields = ['id', 'first_name', 'last_name', 'surname2', 'gender', 'id_number', 'email', 'fake_email', 'birthdate',
              'birth_place', 'town', 'district', 'address', 'phone_number', 'educational_level',
              'employment_situation', 'discovered_us', 'cooperativism_knowledge', 'authorize_communications',
              'project', 'is_staff', 'groups',
              'is_active', 'date_joined', 'last_login', ]
    readonly_fields = ['id', 'last_login', 'date_joined', 'project', ]
    actions = ['copy_emails', ]

    def project(self, obj):
        if obj.project:
            return mark_safe(f"<a href=\"../../../project/{ obj.project.id }/change/\">{ obj.project }</a>")
        return None
    project.short_description = 'Projecte'

    def get_fields(self, request, obj=None):
        if request.user.is_superuser and "is_superuser" not in self.fields:
            self.fields.append('is_superuser')

        if not request.user.is_superuser:
            self.readonly_fields.append('groups')

        # If we are adding a new user, don't show these fields:
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
        # Sending welcome e-mail only if we're creating a new account.
        if not change:
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
