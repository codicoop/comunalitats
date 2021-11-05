
from django.apps import apps
from django.contrib.auth import get_user_model
from apps.cc_lib import DjangoFactory


class UserFactory(DjangoFactory):
    class Meta:
        model = get_user_model()


class ProjectFactory(DjangoFactory):
    class Meta:
        model = apps.get_model('coopolis', 'Project')
