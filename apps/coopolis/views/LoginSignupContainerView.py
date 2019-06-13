#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cc_users.views import LoginView
from cc_users.views import SignUpView
from django.views.generic import TemplateView
from coopolis.models import User
from coopolis.forms import MySignUpForm
from cc_users.forms import LogInForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django import urls
from django.core.mail import send_mail
from django.conf import settings
from constance import config


class LoginSignupContainerView(TemplateView):
    template_name = 'registration/login_signup_container.html'

    def get(self, request, *args, **kwargs):
        login_form = LogInForm
        signup_form = MySignUpForm
        context = self.get_context_data(**kwargs)
        context['login_form'] = login_form
        context['signup_form'] = signup_form
        return self.render_to_response(context)


class CoopolisSignUpView(SignUpView):
    template_name = 'registration/login_signup_container.html'
    success_url = '/'
    form_class = MySignUpForm
    model = User

    def form_invalid(self, form):
        login_form = LogInForm
        return self.render_to_response(
            self.get_context_data(login_form=login_form, signup_form=form)
        )

    def get_success_url(self):
        if 'next' in self.request.GET:
            url = self.request.GET.get('next') + '?' + self.request.GET.urlencode()
        else:
            url = self.request.META.get('HTTP_REFERER')
        if url is None:
            url = super().get_success_url()
        return url

    def form_valid(self, form):
        form.save()
        self.send_welcome_email(self.request.POST['email'])
        username = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(urls.reverse('loginsignup'))

    # TODO: Aquesta funció està duplicada a UserAdmin. Decidir si ficar-la com a helper? O fitxer de funcions de mail?
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


class CoopolisLoginView(LoginView):
    template_name = 'registration/login_signup_container.html'
    success_url = '/'
    form_class = LogInForm

    def form_invalid(self, form):
        signup_form = MySignUpForm
        return self.render_to_response(
            self.get_context_data(login_form=form, signup_form=signup_form)
        )

    def get_success_url(self):
        if 'next' in self.request.GET:
            url = self.request.GET.get('next') + '?' + self.request.GET.urlencode()
        else:
            url = self.request.META.get('HTTP_REFERER')
        if url is None:
            url = super().get_success_url()
        return url

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(urls.reverse('loginsignup'))
