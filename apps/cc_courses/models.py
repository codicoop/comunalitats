from django.db import models
from cc_lib.utils import slugify_model
from .utils import get_enrollable_class
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from uuid import uuid4
from apps.cc_courses.exceptions import EnrollToActivityNotValidException
from datetime import date


def upload_path(instance, filename):
    if isinstance(instance, Course):
        return 'course.banner/{0}/banner.png'.format(str(uuid4()), filename)


class CoursePlace(models.Model):
    class Meta:
        verbose_name = "Lloc"

    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
    address = models.CharField("Adreça", max_length=200)

    def __str__(self):
        return self.name


class Entity(models.Model):
    class Meta:
        verbose_name = "Entitat"

    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
    legal_id = models.CharField("C.I.F.", max_length=9)
    # TODO: Validate CIF format.

    def __str__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = "Formació"
        verbose_name_plural = "Formacions"
        ordering = ["date_start"]

    title = models.CharField("Títol", max_length=250, blank=False)
    slug = models.CharField(max_length=250, unique=True)
    date_start = models.DateField("Dia inici")
    date_end = models.DateField("Dia finalització", null=True, blank=True)
    hours = models.CharField("Horaris", blank=False, max_length=200,
                             help_text="Indica només els horaris, sense els dies.")
    description = models.TextField("Descripció", null=True)
    published = models.BooleanField("Publicat")
    created = models.DateTimeField(null=True, blank=True)
    banner = models.ImageField(null=True, upload_to=upload_path, max_length=250)

    # Fields currently not needed:
    # spots = models.IntegerField('Places totals', default=0)
    # enrolled = models.ManyToManyField(get_enrollable_class(), blank=True, related_name='enrolled_courses')
    # place = models.ForeignKey("CoursePlace", on_delete=models.SET_NULL, null=True)
    #
    # @property
    # def remaining_spots(self):
    #    return self.spots - self.enrolled.count()

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')

    @property
    def absolute_url(self):
        if self.slug:
            return reverse('course', args=[str(self.slug)])
        return None

    def __str__(self):
        return self.title


class Activity(models.Model):
    class Meta:
        verbose_name = "Activitat"
        ordering = ["date_start"]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Formació / Programa")
    name = models.CharField("Títol", max_length=200, blank=False, null=False)
    objectives = models.TextField("Descripció", null=True)
    place = models.ForeignKey(CoursePlace, on_delete=models.SET_NULL, null=True,
                              verbose_name="Lloc")
    date_start = models.DateField("Dia inici")
    date_end = models.DateField("Dia finalització", blank=True, null=True)
    starting_time = models.TimeField("Hora d'inici")
    ending_time = models.TimeField("Hora de finalització")
    spots = models.IntegerField('Places totals', default=0)
    enrolled = models.ManyToManyField(get_enrollable_class(), blank=True, related_name='enrolled_activities',
                                      verbose_name="Inscrites")
    ORGANIZER_OTIONS = (
        ('AT', 'Ateneu'),
        ('CM', 'Cercle Migracions'),
        ('CI', "Cercle Incubació"),
        ('CC', 'Cercle Consum')
    )
    organizer = models.TextField("Qui ho organitza", choices=ORGANIZER_OTIONS)
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True)
    AXIS_OPTIONS = (
        ('A', 'Eix A'),
        ('B', 'Eix B'),
        ('C', "Eix C"),
        ('D', 'Eix D')
    )
    axis = models.TextField("Eix", help_text="Eix de la convocatòria on es justificarà.", choices=AXIS_OPTIONS,
                            null=True, blank=True)
    published = models.BooleanField("Publicada", default=True)

    @property
    def remaining_spots(self):
        return self.spots - self.enrolled.count()

    def enroll_user(self, user):
        if user in self.enrolled.all():
            raise EnrollToActivityNotValidException()
        self.enrolled.add(user)
        self.save()

    def __str__(self):
        return self.name

    @property
    def absolute_url(self):
        return self.course.absolute_url

    @property
    def is_past_due(self):
        return date.today() > self.date_start


pre_save.connect(Course.pre_save, sender=Course)
