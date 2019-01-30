#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .admin import coopolis_admin_site
from .views import ProjectFormView, SignUp, LogIn, ProjectCreateFormView, ProjectInfoView
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url('admin/login', RedirectView.as_view(pattern_name=settings.LOGIN_URL, permanent=True, query_string=True)),
]

urlpatterns += [
    path('', TemplateView.as_view(
        template_name="home.html",
        extra_context={
            'courses_title': "Formació i activitats",
            'courses_text': "TEXT D'INTRODUCCIÓ A LES FORMACIONS QUE FEM",
            'projects_title': "Acompanyament de projectes",
            'projects_text': "TEXT D'INTRODUCCIÓ A L'ACOMPANYAMENT DE PROJECTES"
        }
    ), name='home'),
    path('login/', LogIn.CoopolisLoginView.as_view(), name='login'),
    path('users/login/', LogIn.CoopolisLoginView.as_view(), name='login'),
    path('signup', SignUp.signup, name='signup'),
    path('admin/', coopolis_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('project/edit/', login_required(ProjectFormView.as_view()), name='edit_project'),
    path('project/new/', login_required(ProjectCreateFormView.as_view()), name='new_project'),
    path('project/info/', ProjectInfoView.as_view(), name='project_info'),
]
