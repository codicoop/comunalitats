#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from coopolis.models import Project, User
from cc_users.forms import SignUpForm


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['project_responsible']


class MySignUpForm(SignUpForm):
    first_name = forms.CharField(label="Nom", max_length=30, required=False, help_text='Opcional.')

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['is_confirmed', 'groups', 'user_permissions', 'is_staff', 'is_active',
                   'is_superuser', 'last_login', 'date_joined', 'project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
