#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from coopolis.models import Project, User, ProjectStage
from cc_courses.models import Activity
from django.contrib.auth.forms import UserCreationForm
from coopolis.widgets import XDSoftDatePickerInput
from django.utils.safestring import mark_safe
from constance import config
from coopolis.mixins import FormDistrictValidationMixin
from dynamic_fields.fields import DynamicChoicesWidget
from django.conf import settings


class ProjectForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['cif', 'registration_date', 'constitution_date', 'partners']


class ProjectFormAdmin(ProjectForm):
    class Meta:
        # Un-excluding the fields that we were hiding for the front-end.
        exclude = None


class MySignUpForm(FormDistrictValidationMixin, UserCreationForm):
    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False)
    email = forms.EmailField(
        label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')
    birthdate = forms.DateField(label="Data de naixement", required=False, widget=XDSoftDatePickerInput())
    accept_conditions = forms.BooleanField(
        label="He llegit i accepto", required=True)
    accept_conditions2 = forms.BooleanField(
        label="He llegit i accepto", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'phone_number', 'birthdate',
                  'birth_place', 'town', 'district', 'address', 'gender', 'educational_level',
                  'employment_situation', 'discovered_us', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

        self.fields['accept_conditions'].help_text = mark_safe(config.CONTENT_SIGNUP_LEGAL1)
        self.fields['accept_conditions2'].help_text = mark_safe(config.CONTENT_SIGNUP_LEGAL2)


class MySignUpAdminForm(MySignUpForm):
    password = forms.CharField(required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    accept_conditions = forms.BooleanField(required=False)
    accept_conditions2 = forms.BooleanField(required=False)


def get_item_choices(model, value):
    choices = []

    item = sorted(settings.SUBAXIS_OPTIONS[value])

    for thing in item:
        choices.append({
            'value': thing[0],
            'label': thing[1],
        })

    return choices


class ProjectStageForm(forms.ModelForm):
    class Meta:
        model = ProjectStage
        fields = '__all__'
        widgets = {
            'subaxis': DynamicChoicesWidget(
                depends_field='axis',
                model=ProjectStage,  # This is supposed to be the model of a FK, but our subaxis field is not a FK
                                     # but a dictionary in the settings. Turns out that it only wants the model to
                                     # take its name and use it as identifier when rendering the HTML, so now that
                                     # get_item_choices() is not using the model to return the values, we can put here
                                     # any model, as a workaround.
                                     # Best quality solution would be modify the library to make it model-optional.
                callback=get_item_choices,
                no_value_disable=True,
                include_empty_choice=True,
                empty_choice_label="Selecciona un sub-eix",
            )
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        widgets = {
            'subaxis': DynamicChoicesWidget(
                depends_field='axis',
                model=Activity,  # This is supposed to be the model of a FK, but our subaxis field is not a FK
                                     # but a dictionary in the settings. Turns out that it only wants the model to
                                     # take its name and use it as identifier when rendering the HTML, so now that
                                     # get_item_choices() is not using the model to return the values, we can put here
                                     # any model, as a workaround.
                                     # Best quality solution would be modify the library to make it model-optional.
                callback=get_item_choices,
                no_value_disable=True,
                include_empty_choice=True,
                empty_choice_label="Selecciona un sub-eix",
            )
        }
