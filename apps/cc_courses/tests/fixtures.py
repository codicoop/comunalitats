#!/usr/bin/env python
# -*- coding: utf-8 -*-

import factory
from factory import fuzzy
from faker import Faker
import datetime
from django.conf import settings
from django.utils import timezone
from django.apps import apps
import random


fake = Faker()


def _get_tzinfo():
    """Fetch the current timezone."""
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class EntityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Entity')
        django_get_or_create = ('name',)

    name = factory.Faker('name')
    legal_id = factory.Faker('address')


class CoursePlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'CoursePlace')
        django_get_or_create = ('name',)

    name = factory.Faker('name')
    address = factory.Faker('address')


class CourseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'CourseCategory')
        django_get_or_create = ('name',)

    name = factory.Faker('name')


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Course')

    title = factory.Faker('text', max_nb_chars=100, ext_word_list=None)
    date_start = fuzzy.FuzzyDate(datetime.date(2018, 11, 1), datetime.date(2019, 6, 26))
    date_end = fuzzy.FuzzyDate(datetime.date(2019, 6, 27), datetime.date(2019, 12, 26))
    hours = factory.Faker('text', max_nb_chars=15, ext_word_list=None)
    description = fake.paragraph(nb_sentences=5, variable_nb_sentences=True, ext_word_list=None)
    published = True
    created = timezone.now()


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Activity')

    name = factory.Faker('text', max_nb_chars=80)
    objectives = fake.paragraph(nb_sentences=5, variable_nb_sentences=True, ext_word_list=None)
    spots = random.randint(10, 40)
    starting_time = "10:00"
    ending_time = "14:00"
    published = True


