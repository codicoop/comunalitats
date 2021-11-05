# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from apps.cc_courses.tests.fixtures import ActivityFactory, CourseFactory
import random
import factory.fuzzy as fuzzy
from django.utils import timezone
import datetime
from apps.cc_courses.models import Entity, Activity
from apps.cc_lib.commands.generate_fakes_command import GenerateFakesCommand
import factory
from apps.cc_lib import tuplelize


class Command(GenerateFakesCommand):
    def create_entitys(self, factory, number=50, related=None):
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

    def create_courses(self, factory, number=50, related=None):
        from apps.cc_lib import fixture_helpers as helpers
        times = {
            'past': {
                'date_start': helpers.one_past_moment_between_days(500, 365),
                'date_end': helpers.one_moment_in_the_last_days(365)
            },
            'future': {
                'date_start': helpers.one_moment_in_the_next_days(100),
                'date_end': helpers.one_future_moment_between_days(100, 365)
            }
        }
        courses = []
        for when in times.values():
            courses.extend(CourseFactory.create_batch(
                size=int(number / len(times)),
                date_start=when['date_start'],
                date_end=when['date_end']
            ))
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Courses'))
        return courses

    def create_activitys(self, _, number=50, related=None):
        courses = self.get_generated_objects('Course')
        course_places = self.get_generated_objects('CoursePlace')
        entities = self.get_generated_objects('Entity')

        activities = ActivityFactory.create_batch(
            size=number,
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
            organizer=factory.Iterator(tuplelize(multidim_list=Activity.ORGANIZER_OTIONS)),
            entity=factory.Iterator(entities),
            axis=factory.Iterator(tuplelize(multidim_list=Activity.AXIS_OPTIONS))
        )
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Course Activities'))
        return activities

    def enroll_users(self):
        users = self.get_generated_objects('User')
        activities = self.get_generated_objects('Activity')
        for activity in activities:
            users_sample = random.sample(users, k=random.randint(2, 10))
            for user in users_sample:
                activity.enroll_user(user)
        self.stdout.write(self.style.SUCCESS('Users randomly enrolled into Activities.'))

    def fakes_generation_finished(self):
        self.enroll_users()

    def tuplelize(self, multidim_list):
        return [i[0] for i in multidim_list]
