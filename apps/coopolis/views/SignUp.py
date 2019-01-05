#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cc_lib.utils import get_class_from_route
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.conf import settings
from cc_users.views import get_activate_url
from django.contrib.auth import login
from django.http import HttpResponseRedirect


def signup(request):
    # TODO: Make this view as class so it's not required to set the settings for the form class, just inherit
    SignUpForm = get_class_from_route(settings.SIGNUP_FORM)

    if request.user and request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            login(request, user)
            subject = 'Activate Your Account'
            message = render_to_string('emails/user_registration.html', {
                'url': get_activate_url(request, user),
                'user': user
            })
            user.email_user(subject, message)

            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url + '?' + request.GET.urlencode())
            else:
                return render(request, 'registration/user_registered.html', {'email': form.cleaned_data.get('email')})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
