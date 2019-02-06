#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .admin import coopolis_admin_site
from .views import ProjectFormView, ProjectCreateFormView, ProjectInfoView, LoginSignupContainerView,\
    CoopolisSignUpView, CoopolisLoginView, HomeView
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from cc_users.decorators import anonymous_required

urlpatterns = [
    url('admin/login', RedirectView.as_view(pattern_name=settings.LOGIN_URL, permanent=True, query_string=True)),
]

urlpatterns += [
    path('', HomeView.as_view(), name='home'),
    path('users/loginsignup/', anonymous_required(LoginSignupContainerView.as_view()), name='loginsignup'),
    path('users/login_post/', anonymous_required(CoopolisLoginView.as_view()), name='login_post'),
    path('users/signup_post', anonymous_required(CoopolisSignUpView.as_view()), name='signup_post'),
    path('admin/', coopolis_admin_site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('project/edit/', login_required(ProjectFormView.as_view()), name='edit_project'),
    path('project/new/', login_required(ProjectCreateFormView.as_view()), name='new_project'),
    path('project/info/', ProjectInfoView.as_view(), name='project_info'),
]
