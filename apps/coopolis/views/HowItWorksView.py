#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic


class HowItWorksView(generic.TemplateView):
    template_name = "how_it_works.html"
    extra_context = {
        'courses_title': "Formació i activitats",
        'courses_text': "TEXT D'INTRODUCCIÓ A LES FORMACIONS QUE FEM",
        'projects_title': "Acompanyament de projectes",
        'projects_text': "TEXT D'INTRODUCCIÓ A L'ACOMPANYAMENT DE PROJECTES"
    }
