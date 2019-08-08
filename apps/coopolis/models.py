from cc_users.models import BaseUser
from django.db import models
from django.conf import settings
from uuid import uuid4
from cc_users.managers import CCUserManager
import datetime
from cc_courses.models import Entity


def stage_certificate_upload_path(instance, filename):
    if isinstance(instance, ProjectStage):
        return 'course.stage_certificate/{0}/{1}'.format(str(uuid4()), filename)


def stage_signatures_upload_path(instance, filename):
    if isinstance(instance, ProjectStage):
        return 'course.stage_signatures/{0}/{1}'.format(str(uuid4()), filename)


def estatuts_upload_path(instance, filename):
    if isinstance(instance, Project):
        return 'course.estatuts/{0}/{1}'.format(str(uuid4()), filename)


def viability_upload_path(instance, filename):
    if isinstance(instance, Project):
        return 'course.pla_viabilitat/{0}/{1}'.format(str(uuid4()), filename)


def sostenibility_upload_path(instance, filename):
    if isinstance(instance, Project):
        return 'course.pla_sostenibilitat/{0}/{1}'.format(str(uuid4()), filename)


class Town(models.Model):
    class Meta:
        verbose_name = "població"
        verbose_name_plural = "poblacions"

    name = models.CharField("nom", max_length=250)

    def __str__(self):
        return self.name


class Project(models.Model):
    class Meta:
        verbose_name_plural = "projectes"
        verbose_name = "projecte"

    partners = models.ManyToManyField('User', verbose_name="sòcies", blank=True, related_name='projects')
    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    SECTORS = (
        ('A', 'Altres'),
        ('C', 'Comunicació i tecnologia'),
        ('F', 'Finances'),
        ('O', 'Oci'),
        ('H', 'Habitatge'),
        ('L', 'Logística'),
        ('E', 'Educació'),
        ('C', 'Cultura'),
        ('S', 'Assessorament'),
        ('M', 'Alimentació'),
        ('U', 'Cures'),
        ('R', 'Roba')
    )
    sector = models.CharField(max_length=2, choices=SECTORS)
    web = models.CharField("Web", max_length=200, blank=True)
    PROJECT_STATUS_OPTIONS = (
        ("IN_MEDITATION_PROCESS", "En proces de debat/reflexió"),
        ("IN_CONSTITUTION_PROCESS", "En constitució"),
        ("RUNNING", "En funcionament"),
        ("DOWN", "Caigut")
    )
    project_status = models.CharField("estat del projecte", max_length=50, blank=True, null=True,
                                      choices=PROJECT_STATUS_OPTIONS)
    MOTIVATION_OPTIONS = (
        ('COOPERATIVISM_EDUCATION', 'Formació en cooperativisme'),
        ('COOPERATIVE_CREATION', "Constitució d'una cooperativa"),
        ('TRANSFORM_FROM_ASSOCIATION', "Transformació d'associació a coopetiva"),
        ('TRANSFORM_FROM_SCP', "Transformació de SCP a coopertiva"),
        ('ENTERPRISE_RELIEF', "Relleu empresarial"),
        ('CONSOLIDATION', "Consolidació"),
        ('OTHER', "Altres"),
    )
    motivation = models.CharField("petició inicial", max_length=50, blank=True, null=True, choices=MOTIVATION_OPTIONS)
    mail = models.EmailField("correu electrònic")
    phone = models.CharField("telèfon", max_length=25)
    town = models.ForeignKey(Town, verbose_name="població", on_delete=models.SET_NULL, null=True, blank=True)
    district = models.TextField("districte", blank=True, null=True, choices=settings.DISTRICTS)
    number_people = models.IntegerField("número de persones", blank=True, null=True)
    registration_date = models.DateField("data de registre", blank=True, null=True, default=datetime.date.today)
    cif = models.CharField("N.I.F.", max_length=11, blank=True, null=True)
    object_finality = models.TextField("objecte i finalitat", blank=True, null=True)
    project_origins = models.TextField("orígens del projecte", blank=True, null=True)
    solves_necessities = models.TextField("quines necessitats resol el vostre projecte?", blank=True, null=True)
    social_base = models.TextField("compta el vostre projecte amb una base social?", blank=True, null=True)
    constitution_date = models.DateField("data de constitució", blank=True, null=True)
    estatuts = models.FileField("estatuts", blank=True, null=True, upload_to=estatuts_upload_path, max_length=250)
    viability = models.FileField("pla de viabilitat", blank=True, null=True,
                                 upload_to=estatuts_upload_path, max_length=250)
    sostenibility = models.FileField("pla de sostenibilitat", blank=True, null=True,
                                     upload_to=estatuts_upload_path, max_length=250)

    @property
    def has_estatus(self):
        if self.estatuts:
            return True
        else:
            return False

    @property
    def has_viability(self):
        if self.viability:
            return True
        else:
            return False

    @property
    def has_sostenibility(self):
        if self.sostenibility:
            return True
        else:
            return False

    def __str__(self):
        return self.name


class User(BaseUser):
    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "persones"
        ordering = ["first_name"]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CCUserManager()

    fake_email = models.BooleanField("e-mail inventat", default=False,
                                     help_text="Marca aquesta casella si el correu és inventat, i desmarca-la si mai "
                                               "el canvieu pel correu real. Ens ajudarà a mantenir la base de dades"
                                               "neta.")
    username = models.CharField(unique=False, null=True, max_length=150, verbose_name="nom d'usuari/a")
    surname2 = models.CharField("segon cognom", max_length=50, blank=True, null=True)
    id_number = models.CharField("DNI o NIE", null=True, max_length=11)
    GENDERS = (
        ('OTHER', 'Altre'),
        ('FEMALE', 'Dona'),
        ('MALE', 'Home')
    )
    gender = models.CharField("gènere", blank=True, null=True, choices=GENDERS, max_length=10)
    BIRTH_PLACES = (
        ("BARCELONA", "Barcelona"),
        ("CATALUNYA", "Catalunya"),
        ("ESPANYA", "Espanya"),
        ("OTHER", "Altre")
    )
    birth_place = models.TextField("lloc de naixement", blank=True, null=True, choices=BIRTH_PLACES)
    birthdate = models.DateField("data de naixement", blank=True, null=True)
    town = models.ForeignKey(Town, verbose_name="població", on_delete=models.SET_NULL, null=True, blank=True)
    district = models.TextField("districte", blank=True, null=True, choices=settings.DISTRICTS)
    address = models.CharField("adreça", max_length=250, blank=True, null=True)
    phone_number = models.CharField("telèfon", max_length=25, blank=True, null=True)
    STUDY_LEVELS = (
        ('MASTER', 'Màster / Postgrau'),
        ('HIGH_SCHOOL', 'Secundària'),
        ('WITHOUT_STUDIES', 'Sense estudis'),
        ('FP', 'Formació professional'),
        ('UNIVERSITY', 'Estudis universitaris'),
        ('ELEMENTARY_SCHOOL', 'Primària')
    )
    educational_level = models.TextField("nivell d'estudis", blank=True, null=True, choices=STUDY_LEVELS)
    EMPLOYMENT_OPTIONS = (
        ('SELF_EMPLOYED', 'En actiu per compte propi'),
        ('UNEMPLOYMENT_BENEFIT_RECEIVER', 'Perceptora de prestacions socials'),
        ('UNEMPLOYMENT_BENEFIT_REQUESTED', "Demandant d'ocupació"),
        ('EMPLOYED_WORKER', 'En actiu per compte aliè')
    )
    employment_situation = models.TextField("situació laboral", blank=True, null=True, choices=EMPLOYMENT_OPTIONS)
    DISCOVERED_US_OPTIONS = (
        ('INTERNET', 'Per internet i xarxes socials'),
        ('FRIEND', "A través d'un conegut"),
        ('PREVIOUS_ACTIVITY', "Per una activitat de "+settings.PROJECT_NAME),
        ('OTHER', 'Altres')
    )
    discovered_us = models.TextField("com ens has conegut", blank=True, null=True, choices=DISCOVERED_US_OPTIONS)
    cooperativism_knowledge = models.TextField("coneixements previs",
                                               help_text="Tens coneixements / formació / experiència en "
                                                         "cooperativisme? Quina? Cursos realitzats?",
                                               blank=True, null=True)

    @staticmethod
    def autocomplete_search_fields():
        filter_by = "id__iexact", "email__icontains", "first_name__icontains", "id_number__contains", \
                    "last_name__icontains", "surname2__icontains"
        return filter_by

    def enrolled_activities_count(self):
        return self.enrolled_activities.all().count()

    enrolled_activities_count.short_description = "Sessions"

    @property
    def project(self):
        if self.projects.count() > 0:
            return self.projects.all()[0]
        return None

    def get_full_name(self):
        name = self.first_name
        if self.surname:
            name = name + " " + self.surname
        return name

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def surname(self):
        surname = ""
        if self.last_name:
            surname = surname + " " + self.last_name
        if self.surname2:
            surname = surname + " " + self.surname2
        return surname

    def __str__(self):
        return self.get_full_name()


class ProjectStage(models.Model):
    class Meta:
        verbose_name = "justificació d'acompanyament"
        verbose_name_plural = "justificacions d'acompanyaments"
        ordering = ["-date_start"]

    DEFAULT_STAGE_TYPE = 1

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="projecte acompanyat")
    STAGE_TYPE_OPTIONS = (
        ('1', "00 Nova creació - acollida"),
        ('2', "01 Nova creació - procés"),
        ('6', "02 Nova creació - constitució"),
        ('7', "03 Consolidació - 1a acollida"),
        ('8', "04 Consolidació - acompanyament")
    )
    stage_type = models.CharField("tipus d'acompanyament", max_length=2, default=DEFAULT_STAGE_TYPE,
                                  choices=STAGE_TYPE_OPTIONS)
    subsidy_period = models.CharField("convocatòria", blank=True, null=True, max_length=4, default=2019,
                                      choices=settings.SUBSIDY_PERIOD_OPTIONS)
    date_start = models.DateField("data d'inici", null=True, blank=True, default=datetime.date.today)
    date_end = models.DateField("data de finalització", null=True, blank=True)
    follow_up = models.TextField("seguiment", null=True, blank=True)
    axis = models.CharField("eix", help_text="Eix de la convocatòria on es justificarà.", choices=settings.AXIS_OPTIONS,
                            null=True, blank=True, max_length=1)
    subaxis = models.CharField("sub-eix", help_text="Correspon a 'Tipus d'acció' a la justificació.",
                               null=True, blank=True, max_length=2)
    organizer = models.ForeignKey(Entity, verbose_name="qui ho fa", default=None, null=True, blank=True,
                                  on_delete=models.SET_NULL)
    stage_responsible = models.ForeignKey(
        "User", verbose_name="persona responsable", blank=True, null=True, on_delete=models.SET_NULL,
        related_name='stage_responsible', help_text="Persona de l'equip al càrrec de l'acompanyament. Per aparèixer "
        "al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.")
    scanned_signatures = models.FileField("fitxa de projectes (document amb signatures)", blank=True, null=True,
                                          upload_to=stage_signatures_upload_path, max_length=250)
    scanned_certificate = models.FileField("certificat", blank=True, null=True,
                                           upload_to=stage_certificate_upload_path, max_length=250)
    hours = models.IntegerField("número d'hores", help_text="Camp necessari per la justificació.", null=True,
                                blank=True)
    involved_partners = models.ManyToManyField(User, verbose_name="persones involucrades", blank=True,
                                               related_name='stage_involved_partners')

    def __str__(self):
        return str(self.project)
