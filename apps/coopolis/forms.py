#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from coopolis.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
