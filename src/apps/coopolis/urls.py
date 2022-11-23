from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from .views import (
    HomeView, CustomPasswordResetView, ActivityPollView, get_sub_services
)

urlpatterns = [
    url(
        'admin/login', RedirectView.as_view(
            pattern_name=settings.LOGIN_URL, permanent=True, query_string=True
        )
    ),
]

urlpatterns += [
    path('', HomeView.as_view(), name='home'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/docs/', TemplateView.as_view(
        template_name="admin/docs.html"
    ), name='docs'),
    path('summernote/', include('django_summernote.urls')),
    path('email_template_test/', TemplateView.as_view(
        template_name="emails/base.html"), name='email_template_test'),
    path('users/password_reset/',
         CustomPasswordResetView.as_view(), name='password_reset'),
    path('reservations/', include('apps.facilities_reservations.urls')),
    path('activities/<uuid:uuid>/poll',
         ActivityPollView.as_view(), name='activity_poll'),
    path('chained_dropdowns/get_sub_services/', get_sub_services),

    path('admin/', admin.site.urls),
]
