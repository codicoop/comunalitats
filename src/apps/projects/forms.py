from django import forms
from django.core.exceptions import ValidationError
from django.forms import models
from django.urls import reverse

from django.utils.safestring import mark_safe

from apps.projects.models import Project
from apps.coopolis.mixins import FormDistrictValidationMixin


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
            "birth_place": "- Lloc de naixement.<br />",
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
