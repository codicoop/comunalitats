#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cc_lib.utils import get_class_from_route
from django.conf import settings
from django.views.generic import CreateView
from coopolis.models import User
from django import urls
from cc_users.views import SignUpView


class SignUpView(SignUpView):
    form_class = get_class_from_route(settings.SIGNUP_FORM)
    model = User
    template_name = 'registration/signup.html'

