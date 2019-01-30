#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .admin import coopolis_admin_site
from .views import ProjectFormView, SignUp, LogIn, ProjectCreateFormView
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView


urlpatterns = [
    url('admin/login', RedirectView.as_view(pattern_name=settings.LOGIN_URL, permanent=True, query_string=True)),
]

urlpatterns += [
    path('', TemplateView.as_view(
        template_name="home.html",
        extra_context={
            # The lambda makes this expression to be executed each call of home (because of the admin updates)
            'courses_text': "TEXT D'INTRODUCCIÓ A LES FORMACIONS QUE FEM",
            'projects_text': "Lorem ipsum TEXT D'INTRODUCCIÓ A L'ACOMPANYAMENT DE PROJECTES"
        }
    ), name='home'),
    path('login/', LogIn.CoopolisLoginView.as_view(), name='login'),
    path('users/login/', LogIn.CoopolisLoginView.as_view(), name='login'),
    path('signup', SignUp.signup, name='signup'),
    path('admin/', coopolis_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('project/', ProjectFormView.as_view(), name='project'),
    path('project/new/', ProjectCreateFormView.as_view(), name='new_project'),
]
