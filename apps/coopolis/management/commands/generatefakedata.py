# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
import factory
from apps.coopolis.tests.fixtures import UserFactory, ProjectFactory
from apps.cc_courses.tests.fixtures import CourseFactory, CourseCategoryFactory, CoursePlaceFactory

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

    def create_projects(self, n_projects=50):
        projects = ProjectFactory.create_batch(size=n_projects)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Projects'))
        return projects

    def create_course_places(self, n_places=5):
        course_places = CoursePlaceFactory.create_batch(size=n_places)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Course Places'))
        return course_places

    def create_course_categories(self, n_categories=5):
        categories = CourseCategoryFactory.create_batch(size=n_categories)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Course Categories'))
        return categories

    def create_courses(self, course_categories, course_places, n_courses=50):
        courses = CourseFactory.create_batch(
            size=n_courses,
            place=factory.Iterator(course_places),
            category=factory.Iterator(course_categories)
        )
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Courses'))
        return courses

    def create_activities(self, courses, n_activities=200):
        activities = CourseCategoryFactory.create_batch(
            size=n_activities,
            course=factory.Iterator(courses)
        )
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Course Activities'))
        return activities

    def handle(self, *args, **options):
        is_test = options['is-test']
        n_users = options['users']
        assert settings.DEBUG or is_test
        Flush().handle(interactive=not is_test, database=DEFAULT_DB_ALIAS, **options)
        self.create_users(n_users=n_users)
        self.create_projects()
        course_places = self.create_course_places()
        course_categories = self.create_course_categories()
        courses = self.create_courses(course_categories = course_categories, course_places = course_places)
        #TODO Uncomment quan el model estigui canviat pel ForeignKey:
        #self.create_activities(courses=courses)
