#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django import urls
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
