# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
import factory
from apps.coopolis.tests.fixtures import UserFactory, ProjectFactory
from apps.cc_courses.tests.fixtures import ActivityFactory, CourseFactory, CourseCategoryFactory, CoursePlaceFactory
import random
import urllib.request as request
import tempfile
from django.core.files import File
import factory.fuzzy as fuzzy
from cc_lib.utils import storage_files
from django.utils import timezone
import datetime
from cc_courses.models import Entity, Activity


class Command(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test', '--test', action='store_true', dest='is-test'
        )
        parser.add_argument(
            '--users', '--users', action='store', type=int, dest='users', default=25
        )

    def create_entities(self):
        entities = [
            Entity(
                name="Ateneu cooperatiu",
                legal_id="G66622002"
            ),
            Entity(
                name="Cercle de mar",
                legal_id="G66622003"
            ),
            Entity(
                name="Cercle B",
                legal_id="G66622004"
            )
        ]
        Entity.objects.bulk_create(entities)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Entities'))
        return entities

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

    def create_courses(self, n_courses=20):
        times = {
            'past': {
                'date_start': fuzzy.FuzzyDateTime(
                    start_dt=timezone.now() - datetime.timedelta(days=500),
                    end_dt=timezone.now() - datetime.timedelta(days=365)
                ),
                'date_end': fuzzy.FuzzyDateTime(
                    start_dt=timezone.now() - datetime.timedelta(days=365),
                    end_dt=timezone.now()
                )
            },
            'future': {
                'date_start': fuzzy.FuzzyDateTime(
                    start_dt=timezone.now(),
                    end_dt=timezone.now() + datetime.timedelta(days=100)
                ) ,
                'date_end': fuzzy.FuzzyDateTime(
                    start_dt=timezone.now() + datetime.timedelta(days=100),
                    end_dt=timezone.now() + datetime.timedelta(days=365)
                )
            }
        }
        courses = []
        for when in times.values():
            courses.extend(CourseFactory.create_batch(
                size=int(n_courses / len(times)),
                banner=fuzzy.FuzzyChoice(
                    storage_files(
                        settings.FIXTURES_PATH_TO_COURSE_IMAGES,
                        f'http://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}'
                    )
                ),
                date_start=when['date_start'],
                date_end=when['date_end']
            ))
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Courses'))
        return courses

    def create_activities(self, courses, course_places, entities, n_activities=200):
        activities = ActivityFactory.create_batch(
            size=n_activities,
            course=factory.Iterator(courses),
            place=factory.Iterator(course_places),
            date_start=fuzzy.FuzzyDateTime(
                start_dt=timezone.now(),
                end_dt=timezone.now() + datetime.timedelta(days=100)
            ),
            date_end=fuzzy.FuzzyDateTime(
                start_dt=timezone.now() + datetime.timedelta(days=100),
                end_dt=timezone.now() + datetime.timedelta(days=365)
            ),
            organizer=factory.Iterator(Activity.ORGANIZER_OTIONS),
            entity=factory.Iterator(entities),
            axis=factory.Iterator(Activity.AXIS_OPTIONS)
        )
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Course Activities'))
        return activities

    def enroll_users(self, users, activities):
        for activity in activities:
            users_sample = random.sample(users, k=random.randint(2, 10))
            for user in users_sample:
                activity.enroll_user(user)
        self.stdout.write(self.style.SUCCESS('Users randomly enrolled into Activities.'))

    def download_and_upload_images(self, courses):
        def _download_and_upload_images(obj, prop):
            url = str(getattr(obj, prop))
            response = request.urlopen(url)
            data = response.read()
            fp = tempfile.TemporaryFile()
            fp.write(data)
            fp.seek(0)
            setattr(obj, prop, File(fp))
            obj.save()
        [_download_and_upload_images(course, 'banner') for course in courses]
        self.stdout.write(self.style.SUCCESS('Updated courses banner.'))

    def handle(self, *args, **options):
        is_test = options['is-test']
        n_users = options['users']
        assert settings.DEBUG or is_test
        Flush().handle(interactive=not is_test, database=DEFAULT_DB_ALIAS, **options)
        entities = self.create_entities()
        users = self.create_users(n_users=n_users)
        self.create_projects()
        course_places = self.create_course_places()
        course_categories = self.create_course_categories()
        courses = self.create_courses()
        activities = self.create_activities(courses=courses, course_places=course_places, entities=entities)
        self.enroll_users(activities=activities, users=users)
        if not is_test:
            self.download_and_upload_images(courses)
