#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from coopolis.widgets import XDSoftDatePickerInput
from django.utils.safestring import mark_safe
from constance import config
from django.conf import settings
from datetime import datetime
from django.utils.timezone import make_aware

from coopolis.models import Project, User, ProjectStage, ActivityPoll
from cc_courses.models import Activity
from coopolis.mixins import FormDistrictValidationMixin
from dynamic_fields.fields import DynamicChoicesWidget
from facilities_reservations.models import Reservation


class ProjectForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = ('name', 'sector', 'web', 'project_status', 'motivation', 'mail', 'phone', 'town', 'district',
                       'number_people', 'estatuts', 'viability', 'sostenibility', 'object_finality', 'project_origins',
                       'solves_necessities', 'social_base')
        exclude = ['cif', 'registration_date', 'constitution_date', 'partners',]


class ProjectFormAdmin(ProjectForm):
    class Meta:
        # Un-excluding the fields that we were hiding for the front-end.
        exclude = None


class MySignUpForm(FormDistrictValidationMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'phone_number', 'birthdate',
                  'birth_place', 'town', 'district', 'address', 'gender', 'educational_level',
                  'employment_situation', 'discovered_us', 'project_involved', 'password1', 'password2',
                  'authorize_communications']

    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=True)
    email = forms.EmailField(
        label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')
    birthdate = forms.DateField(label="Data de naixement", required=True, widget=XDSoftDatePickerInput())
    accept_conditions = forms.BooleanField(
        label="He llegit i accepto", required=True)
    accept_conditions2 = forms.BooleanField(
        label="He llegit i accepto", required=True)
    authorize_communications = forms.BooleanField(label="Accepto rebre informació sobre els serveis", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

        if "accept_conditions" in self.fields:
            self.fields['accept_conditions'].help_text = mark_safe(config.CONTENT_SIGNUP_LEGAL1)
        if "accept_conditions2" in self.fields:
            self.fields['accept_conditions2'].help_text = mark_safe(config.CONTENT_SIGNUP_LEGAL2)


class MySignUpAdminForm(FormDistrictValidationMixin, forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'phone_number', 'birthdate',
                  'birth_place', 'town', 'district', 'address', 'gender', 'educational_level',
                  'employment_situation', 'discovered_us', 'project_involved', ]

    password = ReadOnlyPasswordHashField()
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False)
    no_welcome_email = forms.BooleanField(label="No enviar correu de benvinguda",
                                          help_text="Al crear un compte per defecte s'enviarà un correu de notificació "
                                                    "amb l'enllaç al back-office i instruccions. Si marqueu aquesta "
                                                    "casella, no s'enviarà.", required=False)
    resend_welcome_email = forms.BooleanField(label="Reenviar correu de benvinguda", required=False,
                                              help_text="Marca aquesta casella si desitges tornar a enviar la "
                                                        "notificació de creació de nou compte.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "town" in self.fields:
            self.fields['town'].required = False

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        if "password" in self.initial:
            return self.initial["password"]
        return None


def get_item_choices(model, value):
    choices = []

    item = sorted(settings.SUBAXIS_OPTIONS[value])

    for thing in item:
        choices.append({
            'value': thing[0],
            'label': thing[1],
        })

    return choices


class ProjectStageInlineForm(forms.ModelForm):
    class Meta:
        model = ProjectStage
        fields = '__all__'

    # S'ha de processar això: settings.SUBAXIS_OPTIONS per convertir-ho en una llista, eliminant el 1r nivell

    choices = [
        (None, '---------')
    ]
    for axis in sorted(settings.SUBAXIS_OPTIONS):
        for subaxis in sorted(settings.SUBAXIS_OPTIONS[axis]):
            choices.append(
                (subaxis[0], subaxis[1])
            )
    subaxis = forms.ChoiceField(choices=choices, label="Sub-eix", required=False)


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
        fields = ('course', 'name', 'objectives', 'place', 'date_start', 'date_end', 'starting_time', 'ending_time',
                  'spots', 'enrolled', 'entity', 'organizer', 'axis', 'subaxis',
                  'photo1', 'photo2', 'publish', 'for_minors', 'minors_school_name', 'minors_school_cif',
                  'minors_grade', 'minors_participants_number', 'minors_teacher', 'room', )
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

    def clean(self):
        super(ActivityForm, self).clean()
        if config.ENABLE_ROOM_RESERVATIONS_MODULE:
            self.synchronize_with_reserved_room()

    def synchronize_with_reserved_room(self):
        change = True if self.instance.pk else False
        obj = self.instance
        # Si és una nova sessió i s'ha seleccionat self.room:
        # Si estem editant una sessió que no tenia una reserva, i ara sí que n'ha de tenir:
        if self.cleaned_data['room'] and (not change or
                                          (change and not obj.room_reservation and self.cleaned_data['room'])):
            # Activity.clean() already checked the availability.
            reservation_obj = self.create_update_reservation()
            obj.room_reservation = reservation_obj

        # Si estem editant una sessió que ja tenia una reserva però han deseleccionat la sala:
        if change and obj.room_reservation and not self.cleaned_data['room']:
            if obj.room_reservation:
                self.delete_reservation()

        # Si estem editant una sessió que ja tenia reserva i que n'ha de continuar tenint:
        if change and obj.room_reservation and self.cleaned_data['room']:
            reservation_obj = self.create_update_reservation(obj.room_reservation)
            obj.room_reservation = reservation_obj

    def create_update_reservation(self, inst=None):
        date_end = self.cleaned_data['date_end'] if self.cleaned_data['date_end'] else self.cleaned_data['date_start']
        values = {
            'title': self.cleaned_data['name'],
            'start': make_aware(datetime.combine(self.cleaned_data['date_start'], self.cleaned_data['starting_time'])),
            'end': make_aware(datetime.combine(date_end, self.cleaned_data['ending_time'])),
            'room': self.cleaned_data['room'],
            'responsible': self.request.user,
            'created_by': self.request.user
        }
        pk = inst.id if inst else None
        obj, created = Reservation.objects.update_or_create(id=pk, defaults=values)
        return obj

    def delete_reservation(self):
        obj = Reservation.objects.filter(id=self.instance.room_reservation.id)
        obj.delete()
        self.instance.room_reservation = None
        self.instance.save()


class ActivityPollForm(FormDistrictValidationMixin, forms.ModelForm):
    class Meta:
        model = ActivityPoll
        fields = (
            # Organització
            'duration', 'hours', 'information', 'on_schedule', 'included_resources', 'space_adequation',
            # Continguts
            'contents',
            # Metodologia
            'methodology_fulfilled_objectives', 'methodology_better_results',
            # Valoració de la persona formadora
            'teacher_has_knowledge', 'teacher_resolved_doubts',
            # Utilitat del curs
            'expectations_satisfied', 'adquired_new_tools', 'met_new_people', 'wanted_start_cooperative',
            # Valoració global
            'general_satisfaction', 'also_interested_in', 'comments'
        )
