from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.conf import settings
from uuid import uuid4
from datetime import date, datetime, time
from easy_thumbnails.fields import ThumbnailerImageField
from django.apps import apps

from cc_lib.utils import slugify_model
from coopolis.managers import Published
from apps.cc_courses.exceptions import EnrollToActivityNotValidException
from coopolis.helpers import get_subaxis_choices


def upload_path(instance, filename):
    if isinstance(instance, Course):
        return 'course.banner/{0}/banner.png'.format(str(uuid4()), filename)


def activity_signatures_upload_path(instance, filename):
    if isinstance(instance, Activity):
        return 'course.activity_signatures/{0}/{1}'.format(str(uuid4()), filename)


def photo1_signatures_upload_path(instance, filename):
    if isinstance(instance, Activity):
        return 'course.activity_photo1/{0}/{1}'.format(str(uuid4()), filename)


def photo2_signatures_upload_path(instance, filename):
    if isinstance(instance, Activity):
        return 'course.activity_photo2/{0}/{1}'.format(str(uuid4()), filename)


class CoursePlace(models.Model):
    class Meta:
        verbose_name = "lloc"

    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    town = models.ForeignKey("coopolis.Town", verbose_name="població", on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField("adreça", max_length=200)

    def __str__(self):
        return self.name


class Entity(models.Model):
    class Meta:
        verbose_name = "entitat"
        verbose_name_plural = "entitats"

    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    legal_id = models.CharField("N.I.F.", max_length=9, blank=True, null=True)

    def __str__(self):
        return self.name


class Organizer(models.Model):
    class Meta:
        verbose_name = "organitzadora"
        verbose_name_plural = "organitzadores"

    name = models.CharField("nom", max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = "acció"
        verbose_name_plural = "accions"
        ordering = ["date_start"]

    TYPE_CHOICES = (
        ('F', "Accions educatives"),
        ('A', "Altres accions")
    )
    title = models.CharField("títol", max_length=250, blank=False)
    slug = models.CharField(max_length=250, unique=True)
    date_start = models.DateField("dia inici")
    date_end = models.DateField("dia finalització", null=True, blank=True)
    hours = models.CharField("horaris", blank=False, max_length=200,
                             help_text="Indica només els horaris, sense els dies.")
    description = models.TextField("descripció", null=True)
    publish = models.BooleanField("publicat")
    created = models.DateTimeField("data de creació", null=True, blank=True, auto_now_add=True)
    banner = ThumbnailerImageField(null=True, upload_to=upload_path, max_length=250, blank=True)
    place = models.ForeignKey(CoursePlace, on_delete=models.SET_NULL, null=True, verbose_name="lloc", blank=True,
                              help_text="Aquesta dada de moment és d'ús intern i no es publica.")
    objects = models.Manager()
    published = Published()

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')

    @property
    def absolute_url(self):
        if self.slug:
            return reverse('course', args=[str(self.slug)])
        return None

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains", )

    def __str__(self):
        return f"{self.title} ({self.date_start})"


class Activity(models.Model):
    class Meta:
        verbose_name = "sessió"
        verbose_name_plural = "sessions"
        ordering = ["date_start"]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="acció",
                               related_name="activities")
    name = models.CharField("títol", max_length=200, blank=False, null=False)
    objectives = models.TextField("descripció", null=True)
    place = models.ForeignKey(CoursePlace, on_delete=models.SET_NULL, null=True, verbose_name="lloc")
    date_start = models.DateField("dia inici")
    date_end = models.DateField("dia finalització", blank=True, null=True)
    starting_time = models.TimeField("hora d'inici")
    ending_time = models.TimeField("hora de finalització")
    spots = models.IntegerField('places totals', default=0)
    enrolled = models.ManyToManyField("coopolis.User", blank=True, related_name='enrolled_activities',
                                      verbose_name="inscrites")
    entity = models.ForeignKey(Entity, verbose_name="entitat", on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey(Organizer, verbose_name="organitzadora", on_delete=models.SET_NULL, null=True,
                                  blank=True)
    JUSTIFICATION_CHOICES = (
        ('A', "Ateneus Cooperatius"),
        ('J', "Ajuntament"),
        ('2', "Les 2 - cofinançat")
    )
    justification = models.CharField("justificació", max_length=1, null=True, blank=True, choices=JUSTIFICATION_CHOICES,
                                     default='A')
    axis = models.CharField("eix", help_text="Eix de la convocatòria on es justificarà.", choices=settings.AXIS_OPTIONS,
                            null=True, blank=True, max_length=1)
    subaxis = models.CharField("sub-eix", help_text="Correspon a 'Tipus d'acció' a la justificació.",
                               null=True, blank=True, max_length=2, choices=get_subaxis_choices())
    scanned_signatures = models.FileField("document amb signatures", blank=True, null=True,
                                          upload_to=activity_signatures_upload_path, max_length=250)
    photo1 = models.FileField("fotografia", blank=True, null=True,
                              upload_to=photo1_signatures_upload_path, max_length=250)
    photo2 = models.FileField("document acreditatiu", blank=True, null=True,
                              upload_to=photo2_signatures_upload_path, max_length=250)
    publish = models.BooleanField("publicada", default=True)
    # minors
    for_minors = models.BooleanField(
        "acció dirigida a menors", default=False,
        help_text="Determina el tipus de justificació i en aquest cas, s'han d'omplir els camps relatius a menors.")
    minors_school_name = models.CharField("nom del centre educatiu", blank=True, null=True, max_length=150)
    minors_school_cif = models.CharField("CIF del centre educatiu", blank=True, null=True, max_length=12)
    MINORS_GRADE_OPTIONS = (
        ('PRIM', "Primària"),
        ('ESO', "Secundària obligatòria"),
        ('BATX', "Batxillerat"),
        ('FPGM', "Formació professional grau mig"),
        ('FPGS', "Formació professional grau superior")
    )
    minors_grade = models.CharField("grau d'estudis", blank=True, null=True, max_length=4, choices=MINORS_GRADE_OPTIONS)
    minors_participants_number = models.IntegerField("número d'alumnes participants", blank=True, null=True)
    minors_teacher = models.ForeignKey("coopolis.User", on_delete=models.SET_NULL, verbose_name="docent", null=True,
                                       blank=True)
    # room reservations module
    room_reservation = models.ForeignKey(apps.get_model("facilities_reservations", "Reservation", False),
                                         on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name="related_activities")
    room = models.ForeignKey(apps.get_model("facilities_reservations", "Room", False), on_delete=models.SET_NULL,
                             verbose_name="sala", related_name='activities', null=True, blank=True,
                             help_text="Si selecciones una sala, quan guardis quedarà reservada per la sessió. "
                                       f"<br>Consulta el <a href=\"/reservations/calendar/\" target=\"_blank\">"
                                       "CALENDARI DE RESERVES</a> per veure la disponibilitat.")

    objects = models.Manager()
    published = Published()

    @property
    def remaining_spots(self):
        return self.spots - self.enrolled.count()

    @property
    def absolute_url(self):
        return self.course.absolute_url

    @property
    def is_past_due(self):
        return date.today() > self.date_start

    @property
    def datetime_start(self):
        if isinstance(self.date_start, date) and isinstance(self.starting_time, time):
            return datetime.combine(self.date_start, self.starting_time)
        return None

    @property
    def datetime_end(self):
        if not isinstance(self.ending_time, time):
            return None
        if not isinstance(self.date_end, date):
            if self.datetime_start:
                return datetime.combine(self.date_start, self.ending_time)
        return datetime.combine(self.date_end, self.ending_time)

    def axis_summary(self):
        axis = self.axis if self.axis else '(cap)'
        subaxis = self.subaxis if self.subaxis else '(cap)'
        return f"{axis} - {subaxis}"
    axis_summary.short_description = "Eix - Subeix"
    axis_summary.admin_order_field = 'axis'

    @property
    def subsidy_period(self):
        model = apps.get_model('dataexports', 'SubsidyPeriod')
        # Using date start as the reference one, if an activity last for more than 1 day it should not matter here.
        obj = model.objects.get(date_start__lte=self.date_start, date_end__gte=self.date_start)
        return obj

    def __str__(self):
        return self.name

    def enroll_user(self, user):
        if user in self.enrolled.all():
            raise EnrollToActivityNotValidException()
        self.enrolled.add(user)
        self.save()


pre_save.connect(Course.pre_save, sender=Course)
