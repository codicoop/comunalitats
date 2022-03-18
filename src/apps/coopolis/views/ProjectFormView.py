from django.views import generic
from django import urls
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from constance import config

from apps.coopolis.models import Project
from apps.coopolis.forms import ProjectForm
from apps.coopolis.views import LoginSignupContainerView
from conf.custom_mail_manager import MyMailTemplate


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
        newproject.notify_new_request_to_ateneu(self.request.user.email)

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
