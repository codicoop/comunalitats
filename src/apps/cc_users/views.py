from itertools import islice

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView, PasswordChangeView as BasePasswordChangeView,
)
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django import urls
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetDoneView as BasePasswordResetDoneView
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView

from .decorators import anonymous_required
from apps.cc_users.forms import SignUpForm as SignUpFormClass, MyAccountForm, \
    PasswordResetForm
from apps.coopolis.models import User


class SignUpView(CreateView):
    form_class = SignUpFormClass
    model = get_user_model()
    template_name = 'registration/signup.html'

    def get_success_url(self):
        url = self.request.META.get('HTTP_REFERER')
        if url is None:
            url = urls.reverse('user_profile')
        return url

    def form_valid(self, form):
        form.save()
        username = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class UsersLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return super().resolve_url(self.request.get_redirect_url())


class MyAccountView(SuccessMessageMixin, UpdateView):
    template_name = 'registration/profile.html'
    form_class = MyAccountForm
    model = User
    success_message = "Dades modificades correctament"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return urls.reverse('user_profile')


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
