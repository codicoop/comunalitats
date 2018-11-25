#!/usr/bin/env python
# -*- coding: utf-8 -*-

import factory
from factory import fuzzy
import datetime
from django.conf import settings
from django.utils import timezone
from django.apps import apps
from django.contrib.auth import get_user_model
import lorem

def _get_tzinfo():
    """Fetch the current timezone."""
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user%d" % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'test')
    is_active = True
    is_staff = False
    is_superuser = False
    last_login = fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=10),
        end_dt=timezone.now()
    )
    date_joined = fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=100),
        end_dt=timezone.now() - datetime.timedelta(days=10)
    )

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('coopolis', 'Project')

    sector = factory.Iterator(i[0] for i in Meta.model.SECTORS)
    name = factory.Faker('name')
    web = "example.com"
    mail = "a@example.com"
    phone = "666111000"
    #TODO: Make factory.Faker('web'), factory.Faker('mail') and factory.Faker('phone').
