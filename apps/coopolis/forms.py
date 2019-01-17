#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from coopolis.models import Project
from cc_users.forms import SignUpForm


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['project_responsible']


class MySignUpForm(SignUpForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
