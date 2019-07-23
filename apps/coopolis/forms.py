#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from coopolis.models import Project, User
from django.contrib.auth.forms import UserCreationForm
from coopolis.widgets import XDSoftDatePickerInput
from django.utils.safestring import mark_safe
from constance import config


class ProjectForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['cif', 'registration_date', 'constitution_date', 'partners']


class MySignUpForm(UserCreationForm):
    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False)
    email = forms.EmailField(label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')
    birthdate = forms.DateField(label="Data de naixement", required=False, widget=XDSoftDatePickerInput())
    accept_conditions = forms.BooleanField(
        label="He llegit i accepto", help_text=mark_safe(config.CONTENT_SIGNUP_LEGAL1), required=True)
    accept_conditions2 = forms.BooleanField(
        label="He llegit i accepto", help_text=mark_safe(config.CONTENT_SIGNUP_LEGAL2), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'phone_number', 'birthdate',
                  'birth_place', 'town', 'residence_district', 'address', 'gender', 'educational_level',
                  'employment_situation', 'discovered_us', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    def clean(self):
        cleaned_data = super().clean()
        town = cleaned_data.get("town")
        residence_district = cleaned_data.get("residence_district")

        if str(town) == "BARCELONA" and residence_district is None:
            raise forms.ValidationError(
                "Si la població és Barcelona, cal que omplis el camp Barri."
            )
