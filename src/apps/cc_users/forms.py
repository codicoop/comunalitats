from constance import config
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm, UserChangeForm,
    PasswordResetForm as BasePasswordResetForm, UserCreationForm,
    ReadOnlyPasswordHashField,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.cc_users.models import User
from apps.coopolis.widgets import XDSoftDatePickerInput
from conf.custom_mail_manager import MyMailTemplate


class LogInForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label="Mantenir la sessió oberta"
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = "Correu electrònic o DNI/NIE/Passaport"

    def clean(self):
        super().clean()
        if not self.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)
        return self.cleaned_data


class MyAccountForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'surname2', 'id_number', 'email',
            'phone_number', 'birthdate',
            'gender', 'educational_level',
            'employment_situation', 'discovered_us', 'project_involved',
            'authorize_communications',
        ]

    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False)
    email = forms.EmailField(
        label="Correu electrònic",
        max_length=254,
        help_text='Requerit, ha de ser una adreça vàlida.',
    )
    birthdate = forms.DateField(
        label="Data de naixement",
        required=False,
        widget=XDSoftDatePickerInput(),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')

    def clean_id_number(self):
        model = get_user_model()
        value = self.cleaned_data.get("id_number")
        if (
            model.objects
            .filter(id_number__iexact=value)
            .exclude(id=self.request.user.id)
            .exists()
        ):
            raise ValidationError("El DNI ja existeix.")
        return value


class PasswordResetForm(BasePasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        mail = MyMailTemplate('EMAIL_PASSWORD_RESET')
        mail.to = to_email
        mail.subject_strings = {
            "comunalitat_nom": config.PROJECT_FULL_NAME,
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
            "url_web_comunalitat": config.PROJECT_WEBSITE_URL,
        }
        mail.send()


class MySignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'surname2', 'id_number',
            'cannot_share_id', 'email',
            'phone_number', 'birthdate', 'gender',
            'educational_level', 'employment_situation',
            'discovered_us', 'project_involved', 'password1', 'password2',
            'authorize_communications'
        )

    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=True)
    email = forms.EmailField(
        label="Correu electrònic",
        max_length=254,
        help_text='Ha de ser una adreça vàlida.',
        required=False,
    )
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
        email = self.cleaned_data.get('email')
        cannot_share_id = self.cleaned_data.get('cannot_share_id')
        id_number = self.cleaned_data.get('id_number')
        if not id_number and not cannot_share_id:
            msg = ("Necessitem el DNI, NIF o passaport per justificar la "
                   "participació davant dels organismes públics que financen "
                   "aquestes activitats.")
            self.add_error('id_number', msg)
        if not email and not id_number:
            msg = ("Per crear un compte és necessari indicar el correu "
                   "electrònic o bé omplir el camp DNI/NIE/Passaport.")
            self.add_error(NON_FIELD_ERRORS, msg)
        return self.cleaned_data

    def clean_id_number(self):
        model = get_user_model()
        value = self.cleaned_data.get("id_number")
        if value and model.objects.filter(id_number__iexact=value).exists():
            raise ValidationError("El DNI ja existeix.")
        return value


class MySignUpAdminForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'surname2', 'id_number', 'email',
            'phone_number', 'birthdate', 'gender',
            'educational_level',
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
        self.fields["email"].required = False
        self.fields["id_number"].required = False

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        if "password" in self.initial:
            return self.initial["password"]
        return None

    def clean(self):
        super().clean()
        cannot_share_id = self.cleaned_data.get('cannot_share_id')
        id_number = self.cleaned_data.get('id_number')
        if not id_number and not cannot_share_id:
            msg = ("Necessitem el DNI, NIF o passaport per justificar la "
                   "participació davant dels organismes públics que financen "
                   "aquestes activitats.")
            self.add_error('id_number', msg)
        email = self.cleaned_data.get('email')
        if not email and not id_number:
            msg = ("És necessari indicar el correu "
                   "electrònic o bé omplir el camp DNI/NIE/Passaport.")
            self.add_error(NON_FIELD_ERRORS, msg)
        return self.cleaned_data
