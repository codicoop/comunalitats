from django.conf import settings


def settings_values(request):
    return {'PROJECT_NAME': settings.PROJECT_NAME}
