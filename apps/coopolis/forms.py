#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from coopolis.models import Project, User
from django.contrib.auth.forms import UserCreationForm
from coopolis.widgets import XDSoftDatePickerInput


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['project_responsible']


class MySignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')
    birthdate = forms.DateField(label="Data de naixement", widget=XDSoftDatePickerInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'phone_number', 'birthdate',
                  'birth_place', 'adreca_tipus_via', 'adreca_nom_via', 'adreca_numero', 'adreca_bloc', 'adreca_planta',
                  'adreca_porta', 'residence_town', 'residence_district', 'gender', 'educational_level',
                  'employment_situation', 'discovered_us', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')
