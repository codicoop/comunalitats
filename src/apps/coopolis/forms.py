from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, ReadOnlyPasswordHashField
)
from django.core.exceptions import ValidationError
from django.forms import models
from django.urls import reverse

from apps.coopolis.widgets import XDSoftDatePickerInput
from django.utils.safestring import mark_safe
from constance import config
from django.conf import settings
from datetime import datetime
from django.utils.timezone import make_aware

from apps.coopolis.models import Project, User, ProjectStage, ActivityPoll
from apps.cc_courses.models import Activity, ActivityEnrolled
from apps.coopolis.mixins import FormDistrictValidationMixin
from apps.facilities_reservations.models import Reservation


class ProjectForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = (
            'name', 'sector', 'web', 'project_status', 'motivation', 'mail',
            'phone', 'town', 'district', 'number_people', 'estatuts',
            'viability', 'sostenibility', 'object_finality', 'project_origins',
            'solves_necessities', 'social_base'
        )
        exclude = ('cif', 'registration_date', 'constitution_date',
                   'partners', )


class ProjectFormAdmin(ProjectForm):
    class Meta:
        # Un-excluding the fields that we were hiding for the front-end.
        exclude = None


class EmploymentInsertionInlineFormSet(models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            if 'DELETE' not in data:
                # When there are no rows in the formset it still calls this
                # clean() but with empty data.
                continue
            # Skipping the ones marked for deletion:
            if data['DELETE']:
                continue
            # We're checking for all the rows because trying to check only
            # for new ones will cause problems, as we'll need to check also
            # for rows in which the user has been modified (or make the
            # user row read only when editing).
            # New (unsaved yet) ones will have data['id'] == None
            self.validate_extended_fields(data['user'], data['project'])

    def validate_extended_fields(self, user_obj, project_obj):
        user_obj_errors = {
            "surname": "- Cognom.<br />",
            "gender": "- Gènere. <br/>",
            "birthdate": "- Data de naixement.<br />",
            "town": "- Municipi.<br />",
        }
        user_errors = [value for key, value in user_obj_errors.items() if
                       not getattr(user_obj, key)]

        cif_error = None
        if not project_obj.cif:
            cif_error = ("- NIF (el trobaràs més amunt en aquest mateix "
                         "formulari).<br>")

        if not user_errors and not cif_error:
            return True
        url = reverse(
            'admin:coopolis_user_change',
            kwargs={'object_id': user_obj.id}
        )
        url = f'<a href="{url}" target="_blank">Fitxa de la Persona</a>'
        msg = (f"No s'ha pogut desar la inserció laboral. Hi ha camps del "
               f"Projecte i de les Persones que normalment son opcionals, "
               f"però que per poder justificar les insercions laborals "
               f"son obligatoris.<br>")
        if user_errors:
            msg += f"De la {url}:<br /> {''.join(user_errors)}<br />"
        if cif_error:
            msg += f"De la fitxa del Projecte:<br>{cif_error}"
        raise ValidationError(mark_safe(msg))


class MySignUpForm(FormDistrictValidationMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'surname2', 'id_number',
            'cannot_share_id', 'email',
            'phone_number', 'birthdate', 'birth_place', 'town', 'district',
            'address', 'gender', 'educational_level', 'employment_situation',
            'discovered_us', 'project_involved', 'password1', 'password2',
            'authorize_communications'
        )

    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=True)
    email = forms.EmailField(
        label="Correu electrònic", max_length=254,
        help_text='Requerit, ha de ser una adreça vàlida.')
    birthdate = forms.DateField(
        label="Data de naixement", required=True,
        widget=XDSoftDatePickerInput())
    accept_conditions = forms.BooleanField(
        label="He llegit i accepto", required=True)
    accept_conditions2 = forms.BooleanField(
        label="He llegit i accepto", required=True)
    authorize_communications = forms.BooleanField(
        label="Accepto rebre informació sobre els serveis", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_number'].required = False
        if "accept_conditions" in self.fields:
            self.fields['accept_conditions'].help_text = mark_safe(
                config.CONTENT_SIGNUP_LEGAL1)
        if "accept_conditions2" in self.fields:
            self.fields['accept_conditions2'].help_text = mark_safe(
                config.CONTENT_SIGNUP_LEGAL2)

    def clean(self):
        super().clean()
        cannot_share_id = self.cleaned_data.get('cannot_share_id')
        id_number = self.cleaned_data.get('id_number')
        if not id_number and not cannot_share_id:
            msg = ("Necessitem el DNI, NIF o passaport per justificar la "
                   "participació davant dels organismes públics que financen "
                   "aquestes activitats.")
            self.add_error('id_number', msg)
        return self.cleaned_data


class MySignUpAdminForm(FormDistrictValidationMixin, forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'surname2', 'id_number', 'email',
            'phone_number', 'birthdate', 'birth_place', 'town',
            'district', 'address', 'gender', 'educational_level',
            'employment_situation', 'discovered_us', 'project_involved',
        )

    password = ReadOnlyPasswordHashField()
    new_password = forms.CharField(
        label="Canviar contrasenya",
        help_text=(
            "La contrasenya actual no es pot veure per seguretat. "
            "Però si escrius una contrasenya en aquest camp i deses els "
            "canvis, l'usuari passarà a tenir aquesta nova contrasenya. "
            "Mentre escrius, la contrasenya és visible per tal que puguis "
            "copiar-la i enviar-li a l'usuari."
        ),
        max_length=150,
        required=False
    )
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False)
    no_welcome_email = forms.BooleanField(
        label="No enviar correu de benvinguda",
        help_text="Al crear un compte per defecte s'enviarà un correu de"
                  " notificació amb l'enllaç al back-office i instruccions. "
                  "Si marqueu aquesta casella, no s'enviarà.",
        required=False
    )
    resend_welcome_email = forms.BooleanField(
        label="Reenviar correu de benvinguda", required=False,
        help_text="Marca aquesta casella si desitges tornar a enviar la "
                  "notificació de creació de nou compte."
    )

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

    # S'ha de processar això: settings.SUBAXIS_OPTIONS per convertir-ho en una
    # llista, eliminant el 1r nivell

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
        # TODO: Canviar això per una llibreria actualitzada
        # widgets = {
        #     'subaxis': DynamicChoicesWidget(
        #         depends_field='axis',
        #         # This is supposed to be the model of a FK, but our subaxis
        #         # field is not a FK
        #         # but a dictionary in the settings. Turns out that it only
        #         # wants the model to
        #         # take its name and use it as identifier when rendering the
        #         # HTML, so now that
        #         # get_item_choices() is not using the model to return the
        #         # values, we can put here
        #         # any model, as a workaround.
        #         # Best quality solution would be modify the library to make it
        #         # model-optional.
        #         model=ProjectStage,
        #         callback=get_item_choices,
        #         no_value_disable=True,
        #         include_empty_choice=True,
        #         empty_choice_label="Selecciona un sub-eix",
        #     )
        # }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            'course', 'name', 'objectives', 'place', 'date_start', 'date_end',
            'starting_time', 'ending_time', 'spots', 'enrolled', 'entity',
            'organizer', 'axis', 'subaxis', 'photo1', 'photo2', 'publish',
            'for_minors', 'minors_school_name', 'minors_school_cif',
            'minors_grade', 'minors_participants_number', 'minors_teacher',
            'room',
        )
        # TODO: Canviar això per una llibreria actualitzada
        # widgets = {
        #     'subaxis': DynamicChoicesWidget(
        #         depends_field='axis',
        #         # This is supposed to be the model of a FK, but our subaxis
        #         # field is not a FK
        #         # but a dictionary in the settings. Turns out that it only
        #         # wants the model to
        #         # take its name and use it as identifier when rendering the
        #         # HTML, so now that
        #         # get_item_choices() is not using the model to return the
        #         # values, we can put here
        #         # any model, as a workaround.
        #         # Best quality solution would be modify the library to make it
        #         # model-optional.
        #         model=Activity,
        #         callback=get_item_choices,
        #         no_value_disable=True,
        #         include_empty_choice=True,
        #         empty_choice_label="Selecciona un sub-eix",
        #     )
        # }

    def clean(self):
        super(ActivityForm, self).clean()
        if config.ENABLE_ROOM_RESERVATIONS_MODULE:
            self.synchronize_with_reserved_room()

    def synchronize_with_reserved_room(self):
        change = True if self.instance.pk else False
        obj = self.instance
        # Si és una nova sessió i s'ha seleccionat self.room:
        # Si estem editant una sessió que no tenia una reserva, i ara sí que
        # n'ha de tenir:
        if (
            self.cleaned_data['room']
            and (
                not change
                or (
                    change
                    and not obj.room_reservation
                    and self.cleaned_data['room']
                )
            )
        ):
            # Activity.clean() already checked the availability.
            reservation_obj = self.create_update_reservation()
            obj.room_reservation = reservation_obj

        # Si estem editant una sessió que ja tenia una reserva però han
        # deseleccionat la sala:
        if change and obj.room_reservation and not self.cleaned_data['room']:
            if obj.room_reservation:
                self.delete_reservation()

        # Si estem editant una sessió que ja tenia reserva i que n'ha de
        # continuar tenint:
        if change and obj.room_reservation and self.cleaned_data['room']:
            reservation_obj = self.create_update_reservation(
                obj.room_reservation)
            obj.room_reservation = reservation_obj

    def create_update_reservation(self, inst=None):
        date_end = self.cleaned_data['date_start']
        if self.cleaned_data['date_end']:
            date_end = self.cleaned_data['date_end']
        values = {
            'title': self.cleaned_data['name'],
            'start': make_aware(
                datetime.combine(
                    self.cleaned_data['date_start'],
                    self.cleaned_data['starting_time']
                )
            ),
            'end': make_aware(
                datetime.combine(date_end, self.cleaned_data['ending_time'])),
            'room': self.cleaned_data['room'],
            'responsible': self.request.user,
            'created_by': self.request.user
        }
        pk = inst.id if inst else None
        obj, created = Reservation.objects.update_or_create(
            id=pk, defaults=values)
        return obj

    def delete_reservation(self):
        obj = Reservation.objects.filter(id=self.instance.room_reservation.id)
        obj.delete()
        self.instance.room_reservation = None
        self.instance.save()


class ActivityEnrolledForm(forms.ModelForm):
    class Meta:
        model = ActivityEnrolled
        fields = (
            'user',
        )

    send_enrollment_email = forms.BooleanField(
        label="Enviar notificació d'inscripció",
        required=False,
        help_text="Si fas una inscripció des del panell d'administració, per "
                  "defecte no s'envia el correu. Marca aquesta casella per "
                  "tal que el rebi de la mateixa manera que si s'hagués "
                  "inscrit des de la part pública.")


class ActivityPollForm(forms.ModelForm):
    class Meta:
        model = ActivityPoll
        fields = (
            # Organització
            'duration', 'hours', 'information', 'on_schedule',
            'included_resources', 'space_adequation',
            # Continguts
            'contents',
            # Metodologia
            'methodology_fulfilled_objectives', 'methodology_better_results',
            'participation_system',
            # Valoració de la persona formadora
            'teacher_has_knowledge', 'teacher_resolved_doubts',
            'teacher_has_communication_skills',
            # Utilitat del curs
            'expectations_satisfied', 'adquired_new_tools', 'met_new_people',
            'wanted_start_cooperative',
            'wants_start_cooperative_now',
            # Valoració global
            'general_satisfaction', 'also_interested_in', 'heard_about_it',
            'comments'
        )
        TRUE_FALSE_CHOICES = (
            (True, 'Yes'),
            (False, 'No')
        )
        widgets = {
            'wants_start_cooperative_now': forms.Select(
                choices=TRUE_FALSE_CHOICES)
        }

    def get_grouped_fields(self):
        fieldsets = [
            ("Organització", {
                'fields': [
                    {
                        'name': 'duration',
                        'type': 'stars',
                        'obj': self.fields.get('duration')
                    },
                    {
                        'name': 'hours',
                        'type': 'stars',
                        'obj': self.fields.get('hours')
                    },
                    {
                        'name': 'information',
                        'type': 'stars',
                        'obj': self.fields.get('information')
                    },
                    {
                        'name': 'on_schedule',
                        'type': 'stars',
                        'obj': self.fields.get('on_schedule')
                    },
                    {
                        'name': 'included_resources',
                        'type': 'stars',
                        'obj': self.fields.get('included_resources')
                    },
                    {
                        'name': 'space_adequation',
                        'type': 'stars',
                        'obj': self.fields.get('space_adequation')
                    },
                ]
            }),
            ("Continguts", {
                'fields': [
                    {
                        'name': 'contents',
                        'type': 'stars',
                        'obj': self.fields.get('contents')
                    },
                ]
            }),
            ("Metodologia", {
                'fields': [
                    {
                        'name': 'methodology_fulfilled_objectives',
                        'type': 'stars',
                        'obj': self.fields.get(
                            'methodology_fulfilled_objectives')
                    },
                    {
                        'name': 'methodology_better_results',
                        'type': 'stars',
                        'obj': self.fields.get('methodology_better_results')
                    },
                    {
                        'name': 'participation_system',
                        'type': 'stars',
                        'obj': self.fields.get('participation_system')
                    },
                ]
            }),
            ("Valoració de la persona formadora", {
                'fields': [
                    {
                        'name': 'teacher_has_knowledge',
                        'type': 'stars',
                        'obj': self.fields.get('teacher_has_knowledge')
                    },
                    {
                        'name': 'teacher_resolved_doubts',
                        'type': 'stars',
                        'obj': self.fields.get('teacher_resolved_doubts')
                    },
                    {
                        'name': 'teacher_has_communication_skills',
                        'type': 'stars',
                        'obj': self.fields.get(
                            'teacher_has_communication_skills')
                    },
                ]
            }),
            ("Utilitat del curs", {
                'fields': [
                    {
                        'name': 'expectations_satisfied',
                        'type': 'stars',
                        'obj': self.fields.get('expectations_satisfied')
                    },
                    {
                        'name': 'adquired_new_tools',
                        'type': 'stars',
                        'obj': self.fields.get('adquired_new_tools')
                    },
                    {
                        'name': 'met_new_people',
                        'type': 'yesno',
                        'obj': self.fields.get('met_new_people')
                    },
                    {
                        'name': 'wanted_start_cooperative',
                        'type': 'yesno',
                        'obj': self.fields.get('wanted_start_cooperative')
                    },
                    {
                        'name': 'wants_start_cooperative_now',
                        'type': 'yesno',
                        'obj': self.fields.get('wants_start_cooperative_now')
                    },
                ]
            }),
            ("Valoració global", {
                'fields': [
                    {
                        'name': 'general_satisfaction',
                        'type': 'stars',
                        'obj': self.fields.get('general_satisfaction')
                    },
                    {
                        'name': 'also_interested_in',
                        'type': 'text',
                        'obj': self.fields.get('also_interested_in')
                    },
                    {
                        'name': 'heard_about_it',
                        'type': 'text',
                        'obj': self.fields.get('heard_about_it')
                    },
                    {
                        'name': 'comments',
                        'type': 'text',
                        'obj': self.fields.get('comments')
                    },
                ]
            }),
        ]
        return fieldsets
