
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model

from apps.coopolis.widgets import XDSoftDatePickerInput
from apps.coopolis.mixins import FormDistrictValidationMixin


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Nom", max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(label="Cognoms", max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class LogInForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label="Mantenir la sessió oberta"
    )
    # referer = request.META.get('HTTP_REFERER')

    def clean(self):
        super().clean()
        if not self.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)
        return self.cleaned_data


class MyAccountForm(FormDistrictValidationMixin, UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'phone_number', 'birthdate',
                  'birth_place', 'town', 'district', 'address', 'gender', 'educational_level',
                  'employment_situation', 'discovered_us', 'project_involved', 'authorize_communications', ]

    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False)
    email = forms.EmailField(
        label="Correu electrònic", max_length=254, help_text='Requerit, ha de ser una adreça vàlida.')
    birthdate = forms.DateField(label="Data de naixement", required=False, widget=XDSoftDatePickerInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')
