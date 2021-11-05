from django.apps import AppConfig
from django.conf import settings


class CoursesConfig(AppConfig):
    name = 'apps.cc_courses'
    verbose_name = settings.COURSES_APP_TITLE

    def ready(self):
        import apps.cc_courses.signals
