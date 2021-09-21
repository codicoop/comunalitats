from django.views import generic
from django import urls
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from constance import config

from coopolis.models import Project
from coopolis.forms import ProjectForm
from coopolis.views import LoginSignupContainerView
from coopolis_backoffice.custom_mail_manager import MyMailTemplate


class ProjectFormView(SuccessMessageMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'
    success_message = "Dades del projecte actualitzades correctament."

    def get_success_url(self):
        return urls.reverse('edit_project')

    def get_object(self, queryset=None):
        return self.request.user.project

    def get(self, request):
        if self.request.user.project is None:
            return HttpResponseRedirect(urls.reverse('new_project'))
        return super().get(self, request)


class ProjectCreateFormView(SuccessMessageMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'
    extra_context = {'show_new_project_info': True}

    def get_success_url(self):
        return urls.reverse('edit_project')

    def form_valid(self, form):
        newproject = form.save()
        newproject.partners.add(self.request.user)

        mail = MyMailTemplate('EMAIL_NEW_PROJECT')
        mail.to = config.EMAIL_FROM_PROJECTS.split(',')
        mail.subject_strings = {
            'projecte_nom': newproject.name
        }
        mail.body_strings = {
            'projecte_nom': newproject.name,
            'projecte_telefon': newproject.phone,
            'projecte_email': newproject.mail,
            'usuari_email': self.request.user.email
        }
        mail.send()

        messages.success(
            self.request,
            "S'ha enviat una sol·licitud d'acompanyament del projecte. En els"
            " propers dies et contactarà una persona de l'ateneu per concertar"
            " una primera reunió."
        )
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request):
        if self.request.user.project is not None:
            return HttpResponseRedirect(urls.reverse('edit_project'))
        return super().get(self, request)


class ProjectInfoView(LoginSignupContainerView):
    template_name = "project_info.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.project:
                return HttpResponseRedirect(urls.reverse('edit_project'))
            else:
                return HttpResponseRedirect(urls.reverse('new_project'))
        return super().get(self, request, *args, **kwargs)
