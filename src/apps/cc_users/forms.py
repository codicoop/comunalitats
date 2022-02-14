from constance import config
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, UserChangeForm,
    PasswordResetForm as BasePasswordResetForm,
)
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.coopolis.widgets import XDSoftDatePickerInput
from apps.coopolis.mixins import FormDistrictValidationMixin
from conf.custom_mail_manager import MyMailTemplate


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


class PasswordResetForm(BasePasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        mail = MyMailTemplate('EMAIL_PASSWORD_RESET')
        mail.to = to_email
        mail.subject_strings = {
            "ateneu_nom": config.PROJECT_FULL_NAME,
        }
        password_reset_url = settings.ABSOLUTE_URL + reverse(
            "password_reset_confirm",
            kwargs={
                "uidb64": context["uid"],
                "token": context["token"],
            }
        )
        mail.body_strings = {
            "persona_nom": context["user"].first_name,
            "persona_email": context["email"],
            "absolute_url": settings.ABSOLUTE_URL,
            "password_reset_url": password_reset_url,
            "url_web_ateneu": config.PROJECT_WEBSITE_URL,
        }
        mail.send()
