#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django import urls
from django.http import HttpResponseRedirect
from coopolis.models import Project
from coopolis.forms import ProjectForm


class ProjectFormView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'

    def get_success_url(self):
        return urls.reverse('project')

    def get_object(self, queryset=None):
        return self.model.objects.get(user=self.request.user)

    def get(self, request):
        if self.request.user.project is None:
            return HttpResponseRedirect(urls.reverse('project_info'))
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
        return HttpResponseRedirect(self.get_success_url())


class ProjectInfoView(generic.TemplateView):
    template_name = "project_info.html"
    extra_context = {
        'description': "TEXT QUE EXPLICA DE QUÈ VA L'ACOMPANYAMENT DE PROJECTES BREUMENT"
    }

    def get(self, request):
        if self.request.user.is_authenticated and self.request.user.project:
            return HttpResponseRedirect(urls.reverse('edit_project'))
        return super().get(self, request)
