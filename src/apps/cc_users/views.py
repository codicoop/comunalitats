from itertools import islice

from constance import config
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView, LoginView,
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, TemplateView, CreateView
from django import urls
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetDoneView as BasePasswordResetDoneView
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView

from conf.custom_mail_manager import MyMailTemplate
from .decorators import anonymous_required
from apps.cc_users.forms import MyAccountForm, PasswordResetForm, LogInForm, \
    MySignUpForm
from apps.cc_users.models import User


class MyAccountView(SuccessMessageMixin, UpdateView):
    template_name = 'registration/profile.html'
    form_class = MyAccountForm
    model = User
    success_message = "Dades modificades correctament"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return urls.reverse('user_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class PasswordResetView(BasePasswordResetView):
    form_class = PasswordResetForm

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = form.get_users(form.cleaned_data["email"])
        # get_users is a generator, but our email field is unique.
        # This is the simplest way to retrieve only 1 item from a generator:
        user_list = list(islice(user, 1))
        if len(user_list) == 0 or not user_list[0].is_active:
            error = ValidationError(
                {
                    "email": "El correu indicat no correspon a cap compte "
                    "registrat, si us plau verifica que l'hagis "
                    "escrit correctament."
                },
                code="inexistent_email",
            )
            form.add_error(None, error)
            return super().form_invalid(form)
        return super().form_valid(form)


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PasswordResetDoneView(BasePasswordResetDoneView):
    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PasswordChangeView(BasePasswordChangeView):
    template_name = "registration/password.html"


class LoginSignupContainerView(TemplateView):
    template_name = 'registration/login_signup_container.html'

    def get(self, request, *args, **kwargs):
        login_form = LogInForm
        signup_form = MySignUpForm
        context = self.get_context_data(**kwargs)
        context['login_form'] = login_form
        context['signup_form'] = signup_form
        return self.render_to_response(context)


class SignUpView(CreateView):
    template_name = 'registration/login_signup_container.html'
    success_url = '/'
    form_class = MySignUpForm
    model = User

    def form_invalid(self, form):
        login_form = LogInForm
        return self.render_to_response(
            self.get_context_data(login_form=login_form, signup_form=form)
        )

    def get_success_url(self):
        if 'next' in self.request.GET:
            url = self.request.GET.get('next') + '?' + self.request.GET.urlencode()
        else:
            url = self.request.META.get('HTTP_REFERER')
        if url is None:
            url = urls.reverse('user_profile')
        return url

    def form_valid(self, form):
        form.save()
        self.send_welcome_email(self.request.POST['email'])
        username = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(urls.reverse('loginsignup'))

    def send_welcome_email(self, mail_to):
        mail = MyMailTemplate('EMAIL_SIGNUP_WELCOME')
        mail.to = mail_to
        mail.subject_strings = {
            'comunalitat_nom': config.PROJECT_FULL_NAME
        }
        mail.body_strings = {
            'comunalitat_nom': config.PROJECT_FULL_NAME,
            'url_backoffice': settings.ABSOLUTE_URL,
            'url_accions': f"{settings.ABSOLUTE_URL}{reverse('courses')}",
        }
        mail.send()


class LoginView(LoginView):
    template_name = 'registration/login_signup_container.html'
    success_url = '/'
    form_class = LogInForm

    def form_invalid(self, form):
        signup_form = MySignUpForm
        return self.render_to_response(
            self.get_context_data(login_form=form, signup_form=signup_form)
        )

    def get_success_url(self):
        if 'next' in self.request.GET:
            url = self.request.GET.get('next') + '?' + self.request.GET.urlencode()
        else:
            url = self.request.META.get('HTTP_REFERER')
        if url is None:
            url = super().get_success_url()
        return url

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(urls.reverse('loginsignup'))
