#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import views as auth_views, forms
from constance import config
from django import urls


class CustomPasswordResetForm(forms.PasswordResetForm):
    """
    To make it possible to define the content of the e-mail from Constance
    and at the same time replace contents from the body with calculated
    values, the best way I found so far is injecting it in the context.
    Extra_context was not an option because the values are not calculated
    until later.

    Another option was to create a tag to be able to do that in the template:
    {{ mail_body|replace:haystack,needle }}
    And passing things from the context to the tag.
    """
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        context['mail_body'] = config.MAIL_PASSWORD_RESET.replace(
            '(password_reset_url)',
            context['protocol'] + "://" + context['site_name'] + urls.reverse(
                 'password_reset_confirm', kwargs={'uidb64': context['uid'], 'token': context['token']}
             )
        )
        context['mail_body'] = context['mail_body'].replace(
            '(username)',
            context['user'].get_username()
        )

        return super().send_mail(subject_template_name, email_template_name,
                                 context, from_email, to_email, html_email_template_name)

    def get_users(self, email):
        """Fixing has_usable_password() issue.
        It's fixed since Django 2.1, but we had to rollback to 2.0, which caused that
        many users were not able to recover their passwords:
        https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.has_usable_password
        is_active filter also removed, given that we're not using that.

        This function can be removed as soon as we migrate to >2.0.
        """
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()

        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
        })
        return (u for u in active_users)


class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    html_email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
