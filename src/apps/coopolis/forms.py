from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware

from apps.polls.models import ActivityPoll
from apps.cc_courses.models import Activity, ActivityEnrolled
from apps.facilities_reservations.models import Reservation


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            'course', 'name', 'objectives', 'place', 'date_start', 'date_end',
            'starting_time', 'ending_time', 'spots', 'enrolled', 'entities',
            'organizer', 'photo1', 'photo2', 'publish',
            'for_minors', 'minors_school_name', 'minors_school_cif',
            'minors_grade', 'minors_participants_number', 'minors_teacher',
            'room',
        )

    def clean(self):
        errors = {}
        if self.cleaned_data.get("room"):
            date_end = self.cleaned_data.get("date_start")
            if self.cleaned_data.get("date_end"):
                date_end = self.cleaned_data.get("date_end")
            existing_reservation = getattr(
                self.instance,
                "room_reservation",
                None,
            )
            values = {
                "id": getattr(existing_reservation, "pk", None),
                "title": self.cleaned_data.get("name"),
                "start": make_aware(
                    datetime.combine(
                        self.cleaned_data.get("date_start"),
                        self.cleaned_data.get("starting_time"),
                    )
                ),
                "end": make_aware(
                    datetime.combine(
                        date_end, self.cleaned_data.get("ending_time"),
                    )
                ),
                "room": self.cleaned_data.get("room"),
                "responsible": self.request.user,
                "created_by": self.request.user,
            }
            reservation_obj = Reservation(**values)
            try:
                reservation_obj.clean()
            except ValidationError as error:
                errors.update({"room": ValidationError(error)})
        if errors:
            raise ValidationError(errors)


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
