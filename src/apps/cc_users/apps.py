from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    name = 'apps.cc_users'
    verbose_name = settings.USERS_APP_TITLE if hasattr(settings, 'USERS_APP_TITLE') else 'Users'
