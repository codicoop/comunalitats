#!/usr/bin/env python
# -*- coding: utf-8 -*-

# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
from fok.tests.fixtures import UserFactory
from cc_cms.tests.fixtures import PageFactory


class GenerateFakesCommand(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'

    def handle(self, *args, **options):
        Flush().handle(interactive=False, database=DEFAULT_DB_ALIAS, **options)
        a = UserFactory.create()
        c = UserFactory.create()
        d = PageFactory.create()
        return