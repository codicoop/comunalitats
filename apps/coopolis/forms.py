#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from coopolis.models import Project, User
from django.contrib.auth.forms import UserCreationForm


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['project_responsible']


class MySignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Nom", max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(label="Cognoms", max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')
    birthdate = forms.DateField(widget=forms.SelectDateWidget())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'phone_number', 'birthdate',
                  'birth_place', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')
