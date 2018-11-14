# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
from apps.coopolis.tests.fixtures import UserFactory

class Command(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test', '--test', action='store_true', dest='is-test'
        )
        parser.add_argument(
            '--works', '--works', action='store', type=int, dest='works', default=50
        )
        parser.add_argument(
            '--users', '--users', action='store', type=int, dest='users', default=25
        )

    def create_users(self, n_users=50):
        users = UserFactory.create_batch(size=n_users)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Users'))
        return users

    def handle(self, *args, **options):
        is_test = options['is-test']
        n_users = options['users']
        assert settings.DEBUG or is_test
        Flush().handle(interactive=not is_test, database=DEFAULT_DB_ALIAS, **options)
        self.create_users(n_users=n_users)
