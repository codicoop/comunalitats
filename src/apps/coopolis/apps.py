from django.apps import AppConfig
from django.conf import settings


class CoopolisConfig(AppConfig):
    name = 'apps.coopolis'
    verbose_name = settings.PROJECT_NAME
