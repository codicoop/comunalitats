
import factory
from factory import fuzzy
from faker import Faker
import datetime
from django.conf import settings
from django.utils import timezone
from django.apps import apps
from apps.cc_lib import storage_files


fake = Faker()


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


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Course')

    title = factory.Faker('text', max_nb_chars=100, ext_word_list=None)
    date_start = fuzzy.FuzzyDate(datetime.date(2018, 11, 1), datetime.date(2019, 6, 26))
    date_end = fuzzy.FuzzyDate(datetime.date(2019, 6, 27), datetime.date(2019, 12, 26))
    hours = factory.Faker('text', max_nb_chars=15, ext_word_list=None)
    description = fake.paragraph(nb_sentences=5, variable_nb_sentences=True, ext_word_list=None)
    publish = True
    created = timezone.now()
    banner = fuzzy.FuzzyChoice(
        storage_files(
            settings.FIXTURES_PATH_TO_COURSE_IMAGES,
            f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}'
        )
    )


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Activity')

    name = factory.Faker('text', max_nb_chars=80)
    objectives = fake.paragraph(nb_sentences=5, variable_nb_sentences=True, ext_word_list=None)
    starting_time = "10:00"
    ending_time = "14:00"
    publish = True


