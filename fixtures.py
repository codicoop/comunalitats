#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factory.django import DjangoModelFactory
import factory
import cc_lib.fixture_helpers as helpers


known_attributes = {
    'first_name':  factory.Faker('first_name'),
    'last_name': factory.Faker('last_name'),
    'username': factory.Sequence(lambda n: "user%d" % n),
    'email': factory.Sequence(lambda n: "user%d@email.coop" % n),
    'password': factory.PostGenerationMethodCall('set_password', 'test'),
    'is_active': True,
    'is_staff': False,
    'is_superuser': False,
    'last_login': helpers.one_moment_in_the_last_days(10),
    'date_joined': helpers.one_moment_between_days(100, 10),
    'title': factory.Faker('sentence'),
    'text': factory.Faker('text', max_nb_chars=2000),
    'web': factory.Faker('url'),
    'url': factory.Faker('url'),
    'phone': factory.Faker('phone_number')
}


def set_att_value(cls, field):
    cls._meta.pre_declarations.declarations[field.attname] = known_attributes[field.attname]
    if hasattr(known_attributes[field.attname], 'unroll_context') and hasattr(known_attributes[field.attname], 'call'):
        cls._meta.post_declarations.declarations[field.attname] = known_attributes[field.attname]
    setattr(cls, field.attname, known_attributes[field.attname])
    cls._meta.base_declarations[field.attname] = known_attributes[field.attname]


class DjangoFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    @classmethod
    def _generate(cls, strategy, params):
        fields = cls._meta.model._meta.get_fields(True, True)
        for field in fields:
            hasattr(field, 'attname') \
                and known_attributes.get(field.attname, None) \
                and not cls._meta.pre_declarations.declarations.get(field.attname, None) \
                and set_att_value(cls, field)
        return super(DjangoFactory, cls)._generate(strategy, params)
