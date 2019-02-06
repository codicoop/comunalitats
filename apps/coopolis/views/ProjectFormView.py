#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django import urls
from django.http import HttpResponseRedirect
from coopolis.models import Project
from coopolis.forms import ProjectForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail


class ProjectFormView(SuccessMessageMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'
    success_message = "Dades del projecte actualitzades correctament."

    def get_success_url(self):
        return urls.reverse('edit_project')

    def get_object(self, queryset=None):
        return self.model.objects.get(user=self.request.user)

    def get(self, request):
        if self.request.user.project is None:
            return HttpResponseRedirect(urls.reverse('new_project'))
        return super().get(self, request)


class ProjectCreateFormView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'

    def get_success_url(self):
        return urls.reverse('edit_project')

    def form_valid(self, form):
        newproject = form.save()
        self.request.user.project = newproject
        self.request.user.save()
        send_mail(
            subject="Nova sol·licitud d'acompanyament: "+self.request.user.project.name,
            message=("Nova sol·licitud d'acompanyament\n"
                     "\n"
                     "Nom del projecte: {}\n<br>"
                     "Telèfon de contacte: {}\n<br>"
                     "Correu electrònic de contacte del projecte:{}\n<br>"
                     "Correu electrònic de l'usuari que l'ha creat: {}\n<br>"
                     ).format(
                        self.request.user.project.name,
                        self.request.user.project.phone,
                        self.request.user.project.mail,
                        self.request.user.email
            ),
            recipient_list={"p.picornell@gmail.com", "coopolis.laie@gmail.com"},
            from_email="hola@codi.coop"
        )
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request):
        if self.request.user.project is not None:
            return HttpResponseRedirect(urls.reverse('edit_project'))
        return super().get(self, request)


class ProjectInfoView(generic.TemplateView):
    template_name = "project_info.html"
    extra_context = {
        'description': "TEXT QUE EXPLICA DE QUÈ VA L'ACOMPANYAMENT DE PROJECTES BREUMENT"
    }

    def get(self, request):
        if self.request.user.is_authenticated and self.request.user.project:
            return HttpResponseRedirect(urls.reverse('edit_project'))
        return super().get(self, request)
