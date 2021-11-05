
from django.conf import settings
from importlib import import_module
from django.contrib.auth import get_user_model
from django.apps import apps


def get_courses_list_view_class():
    from .views import CoursesListView
    if hasattr(settings, 'COURSES_LIST_VIEW_CLASS'):
        values = settings.COURSES_LIST_VIEW_CLASS.split('.')
        module = import_module('.'.join(values[:-1]))
        cl = getattr(module, values[-1])
        return cl
    return CoursesListView


def get_enrollable_class():
    if hasattr(settings, 'COURSES_CLASS_TO_ENROLL'):
        values = settings.COURSES_CLASS_TO_ENROLL.split('.')
        if len(values) == 2:
            return apps.get_model(values[0], values[1], require_ready=False)
        else:
            module = import_module('.'.join(values[:-1]))
            cl = getattr(module, values[-1])
            return cl
    return get_user_model()
