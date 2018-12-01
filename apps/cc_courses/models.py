from django.db import models
from cc_lib.utils import slugify_model
from .utils import get_enrollable_class
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from uuid import uuid4


def upload_path(instance, filename):
    if isinstance(instance, Course):
        return 'course.banner/{0}/banner.png'.format(uuid4(), filename)


class Activity(models.Model):
    name = models.CharField("Nom", max_length=200, blank=False, unique=False, default='')
    applications = models.IntegerField('Places totals', default=0)
    enrolled = models.ManyToManyField(get_enrollable_class(), blank=True, related_name='enrolled_activities')
    applications = models.IntegerField('Places totals', default=0)

    @property
    def remain_applications(self):
        return self.applications - self.enrolled.count()


class Course(models.Model):
    title = models.CharField("Títol", max_length=200, blank=False, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    place = models.ForeignKey("CoursePlace", on_delete=models.SET_NULL, null=True)
    date_start = models.DateField("Dia inici")
    date_end = models.DateField("Dia finalització")
    hours = models.CharField("Horaris", blank=False, max_length=200)
    objectives = models.TextField("Objectius")
    category = models.ForeignKey("CourseCategory", on_delete=models.SET_NULL, null=True)
    published = models.BooleanField("Publicat")
    created = models.DateTimeField(null=True, blank=True)
    enrolled = models.ManyToManyField(get_enrollable_class(), blank=True, related_name='enrolled_courses')
    activities = models.ManyToManyField(Activity, blank=True, related_name='courses')
    applications = models.IntegerField('Places totals', default=0)
    banner = models.ImageField(null=True, upload_to=upload_path)

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')

    @property
    def remain_applications(self):
        return self.applications - self.enrolled.count()

    @property
    def absolute_url(self):
        return reverse('course', args=[str(self.slug)])

    def __str__(self):
        return self.title


class CourseCategory(models.Model):
    name = models.CharField("Nom", max_length=200, blank=False, unique=True)


class CoursePlace(models.Model):
    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
    address = models.CharField("Adreça", max_length=200)

    def __str__(self):
        return self.name


pre_save.connect(Course.pre_save, sender=Course)
