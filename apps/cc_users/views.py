from django.shortcuts import render, redirect, reverse
from apps.cc_users.forms import SignUpForm as SignUpFormClass, MyAccountForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from urllib.parse import urljoin
from django.contrib.auth.views import LoginView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from .tokens import AccountActivationTokenGenerator
from django.conf import settings
from django.views.generic import CreateView
from django import urls
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

def get_activate_url(request, user):
    _id = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
    token = AccountActivationTokenGenerator().make_token(user)
    url = reverse('users_activate', args=(_id, token,))
    domain = get_current_site(request).domain
    protocol = 'https' \
        if request.is_secure and not (domain.startswith('127.0.0.1') or domain.startswith('localhost')) \
        else 'http'
    return urljoin(f'{protocol}://{domain}', url)


def activate(request, uuid, token):
    try:
        _id = force_text(urlsafe_base64_decode(uuid))
        user = get_user_model().objects.get(pk=_id)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None \
            and not user.is_active \
            and not user.is_confirmed \
            and AccountActivationTokenGenerator().check_token(user, token):
        user.is_active = True
        user.is_confirmed = True
        user.save()
        login(request, user)
        # TODO: Add successful activation message
        # TODO: Redirect properly (should we take it from settings?)
        return redirect('/')
    else:
        return render(request, 'registration/user_activation_invalid.html')


# TODO: Merge login and signup forms like in Coòpolis + apply anonymous_required decorator to URLs
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


# TODO: Refactor into CBV (use ProjectformView for an example)
def MyAccountView(request):
    user = request.user
    if request.method == 'POST':
        form = MyAccountForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Dades modificades correctament.')
            return HttpResponseRedirect(reverse('user_profile'))
    else:
        form = MyAccountForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'registration/profile.html', context)
