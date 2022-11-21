from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

from .views import ProjectFormView, ProjectCreateFormView, ProjectInfoView


urlpatterns = [
    url(
        'admin/login', RedirectView.as_view(
            pattern_name=settings.LOGIN_URL, permanent=True, query_string=True
        )
    ),
]

urlpatterns += [
    path('project/edit/', login_required(
        ProjectFormView.as_view()), name='edit_project'),
    path('project/new/', login_required(
        ProjectCreateFormView.as_view()), name='new_project'),
    path('project/info/', ProjectInfoView.as_view(), name='project_info'),
]
