from django.apps import AppConfig
from django.conf import settings


class CoursesConfig(AppConfig):
    name = 'cc_courses'
    verbose_name = settings.COURSES_APP_TITLE

    def ready(self):
        import cc_courses.signals
