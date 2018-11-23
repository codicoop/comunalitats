#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse
from coopolis.models import Project
from coopolis.forms import ProjectForm


class ProjectFormView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'

    def get(self, request, *args, **kwargs):
        current_project = self.get_object()
        if request.user not in current_project.members.all():
            return HttpResponse(status=500)
        return super().get(request, *args, **kwargs)
