from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import RedirectView



urlpatterns = [
    url(
        'admin/login', RedirectView.as_view(
            pattern_name=settings.LOGIN_URL, permanent=True, query_string=True
        )
    ),
]