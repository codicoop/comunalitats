#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Nom", max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(label="Cognoms", max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class LogInForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label="Mantingues la sessió oberta"
    )

    def clean(self):
        super().clean()
        if not self.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)
        return self.cleaned_data


class MyAccountForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        # fields = ('username', 'first_name', 'last_name', 'email', )
        fields = UserChangeForm.Meta.fields
        exclude = ['password', 'is_confirmed', 'username', 'groups', 'user_permissions', 'is_staff', 'is_active',
                   'is_superuser', 'last_login', 'date_joined', 'project']

