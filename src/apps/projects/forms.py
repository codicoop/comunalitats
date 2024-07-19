from django import forms
from django.core.exceptions import ValidationError
from django.forms import models
from django.urls import reverse

from django.utils.safestring import mark_safe

from apps.base.helpers import add_justification_required_text_to_field
from apps.projects.models import Project, EmploymentInsertion, ProjectStage


class ProjectForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = (
            'name', 'sector', 'web', 'project_status', 'motivation', 'mail',
            'phone', 'town', 'neighborhood', 'number_people', 'project_origins',
            'social_base'
        )
        exclude = ('registration_date', 'partners', )


class ProjectFormAdmin(ProjectForm):
    class Meta:
        # Un-excluding the fields that we were hiding for the front-end.
        exclude = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sector"] = add_justification_required_text_to_field(
            self.fields["sector"],
        )
        self.fields["name"] = add_justification_required_text_to_field(
            self.fields["name"],
        )
        self.fields["description"] = add_justification_required_text_to_field(
            self.fields["description"],
        )
        self.fields["town"] = add_justification_required_text_to_field(
            self.fields["town"],
        )
        self.fields["neighborhood"] = add_justification_required_text_to_field(
            self.fields["neighborhood"],
        )
        self.fields["partners"] = add_justification_required_text_to_field(
            self.fields["partners"],
            "Dada necessària per la justificació en cas que el "
            "justifiqueu com a Entitat Creada."
        )
        self.fields["mail"] = add_justification_required_text_to_field(
            self.fields["mail"],
            "Dada necessària per la justificació en cas que el "
            "justifiqueu com a Entitat Creada."
        )
        self.fields["phone"] = add_justification_required_text_to_field(
            self.fields["phone"],
            "Dada necessària per la justificació en cas que el "
            "justifiqueu com a Entitat Creada."
        )
        self.fields["entity_name"] = add_justification_required_text_to_field(
            self.fields["entity_name"],
            "Dada necessària per la justificació en cas que el "
            "justifiqueu com a Entitat Creada."
        )
        self.fields["cif"] = add_justification_required_text_to_field(
            self.fields["cif"],
            "Dada necessària per la justificació en cas que el "
            "justifiqueu com a Entitat Creada."
        )
        self.fields["entity_type"] = add_justification_required_text_to_field(
            self.fields["entity_type"],
            "Dada necessària per la justificació en cas que el "
            "justifiqueu com a Entitat Creada."
        )
        self.fields["constitution_date"] = add_justification_required_text_to_field(
            self.fields["constitution_date"],
            "Dada necessària per la justificació en cas que el "
            "justifiqueu com a Entitat Creada."
        )


class ProjectStageFormAdmin(ProjectForm):
    class Meta:
        model = ProjectStage
        fields = (
            'course',
            'project', 'project_sector', 'types', 'stage_type', 'stage_subtype',
            'subsidy_period', 'date_start', 'service', 'sub_service',
            'communality_role', 'networking', 'agents_involved', 'organizer',
            'responsible', 'scanned_certificate', 'involved_partners',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"] = add_justification_required_text_to_field(
            self.fields["course"],
        )
        self.fields["project"] = add_justification_required_text_to_field(
            self.fields["project"],
        )
        self.fields["project_sector"] = add_justification_required_text_to_field(
            self.fields["project_sector"],
        )
        self.fields["stage_type"] = add_justification_required_text_to_field(
            self.fields["stage_type"],
        )
        self.fields["service"] = add_justification_required_text_to_field(
            self.fields["service"],
        )
        self.fields["sub_service"] = add_justification_required_text_to_field(
            self.fields["sub_service"],
        )
        self.fields["communality_role"] = add_justification_required_text_to_field(
            self.fields["communality_role"],
        )
        self.fields["networking"] = add_justification_required_text_to_field(
            self.fields["networking"],
        )
        self.fields["agents_involved"] = add_justification_required_text_to_field(
            self.fields["agents_involved"],
        )
        self.fields["date_start"] = add_justification_required_text_to_field(
            self.fields["date_start"],
        )


class EmploymentInsertionForm(models.ModelForm):
    class Meta:
        model = EmploymentInsertion
        fields = (
            "activity",
            "user",
            "subsidy_period",
            "insertion_date",
            "end_date",
            "contract_type",
            "entity_name",
            "entity_sector",
            "entity_nif",
            "entity_town",
            "entity_neighborhood",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activity"] = add_justification_required_text_to_field(
            self.fields["activity"],
        )
        self.fields["user"] = add_justification_required_text_to_field(
            self.fields["user"],
        )
        self.fields["subsidy_period"] = add_justification_required_text_to_field(
            self.fields["subsidy_period"],
        )
        self.fields["insertion_date"] = add_justification_required_text_to_field(
            self.fields["insertion_date"],
        )
        self.fields["end_date"] = add_justification_required_text_to_field(
            self.fields["end_date"],
        )
        self.fields["contract_type"] = add_justification_required_text_to_field(
            self.fields["contract_type"],
        )
        self.fields["entity_name"] = add_justification_required_text_to_field(
            self.fields["entity_name"],
        )
        self.fields["entity_sector"] = add_justification_required_text_to_field(
            self.fields["entity_sector"],
        )
        self.fields["entity_nif"] = add_justification_required_text_to_field(
            self.fields["entity_nif"],
        )
        self.fields["entity_town"] = add_justification_required_text_to_field(
            self.fields["entity_town"],
        )
        self.fields["entity_neighborhood"] = add_justification_required_text_to_field(
            self.fields["entity_neighborhood"],
        )

    def clean(self):
        super().clean()
        errors = {}
        user = self.cleaned_data.get('user')
        if user:
            try:
                self.validate_extended_fields(user)
            except ValidationError as error:
                    errors.update({"user": ValidationError(error)})
        if errors:
            raise ValidationError(errors)

    def validate_extended_fields(self, user_obj):
        user_obj_errors = {
            "surname": "- Cognom.<br />",
            "gender": "- Gènere. <br/>",
            "birthdate": "- Data de naixement.<br />",
        }
        user_errors = [value for key, value in user_obj_errors.items() if
                       not getattr(user_obj, key)]

        if not user_errors:
            return True
        url = reverse(
            'admin:cc_users_user_change',
            kwargs={'object_id': user_obj.id}
        )
        url = f'<a href="{url}" target="_blank">Fitxa de la Persona</a>'
        msg = (f"No s'ha pogut desar la inserció laboral. Hi ha camps de "
               f"Persones que normalment son opcionals, "
               f"però que per poder justificar les insercions laborals "
               f"son obligatoris.<br>")
        if user_errors:
            msg += f"De la {url}:<br /> {''.join(user_errors)}<br />"
        raise ValidationError(mark_safe(msg))
