from cc_users.models import BaseUser
from django.db import models
from django.conf import settings
from uuid import uuid4
from cc_users.managers import CCUserManager
import datetime


def stage_signatures_upload_path(instance, filename):
    if isinstance(instance, Project):
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


class Project(models.Model):
    class Meta:
        verbose_name_plural = "Projectes"
        verbose_name = "Projecte"

    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
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
        ("RUNNING", "En funcionament")
    )
    project_status = models.CharField("Estat del projecte", max_length=50, blank=True, null=True,
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
    motivation = models.CharField("Petició inicial", max_length=50, blank=True, null=True, choices=MOTIVATION_OPTIONS)
    mail = models.EmailField("Correu electrònic")
    phone = models.CharField("Telèfon", max_length=25)
    DISTRICTS = (
        ('CV', 'Ciutat Vella'),
        ('EX', 'Eixample'),
        ('HG', 'Horta-Guinardó'),
        ('LC', 'Les Corts'),
        ('NB', 'Nou Barris'),
        ('SA', 'Sant Andreu'),
        ('SM', 'Sant Martí'),
        ('ST', 'Sants-Montjuïc'),
        ('SS', 'Sarrià-Sant Gervasi'),
        ('GR', 'Gràcia')
    )
    district = models.TextField("Districte", blank=True, null=True, choices=DISTRICTS)
    number_people = models.IntegerField("Número de persones", blank=True, null=True)
    registration_date = models.DateField("Data de registre", blank=True, null=True, default=datetime.date.today)
    cif = models.CharField("NIF", max_length=11, blank=True, null=True)
    object_finality = models.TextField("Objecte i finalitat", blank=True, null=True)
    project_origins = models.TextField("Orígens del projecte", blank=True, null=True)
    solves_necessities = models.TextField("Quines necessitats resol el vostre projecte?", blank=True, null=True)
    social_base = models.TextField("Compta el vostre projecte amb una base social?", blank=True, null=True)
    constitution_date = models.DateField("Data de constitució", blank=True, null=True)
    estatuts = models.FileField("Estatuts", blank=True, null=True, upload_to=estatuts_upload_path, max_length=250)
    viability = models.FileField("Pla de viabilitat", blank=True, null=True,
                                 upload_to=estatuts_upload_path, max_length=250)
    sostenibility = models.FileField("Pla de sostenibilitat", blank=True, null=True,
                                     upload_to=estatuts_upload_path, max_length=250)

    def __str__(self):
        return self.name


class Town(models.Model):
    class Meta:
        verbose_name = "Població"
        verbose_name_plural = "Poblacions"

    name = models.CharField("Nom", max_length=250)

    def __str__(self):
        return self.name


class User(BaseUser):
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Persones"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CCUserManager()

    username = models.CharField(unique=False, null=True, max_length=150, verbose_name="Nom d'usuari/a")
    surname2 = models.CharField("Segon cognom", max_length=50, blank=True, null=True)
    id_number = models.CharField("DNI o NIE", null=True, max_length=11)
    GENDERS = (
        ('OTHER', 'Altre'),
        ('FEMALE', 'Dona'),
        ('MALE', 'Home')
    )
    gender = models.CharField("Gènere", blank=True, null=True, choices=GENDERS, max_length=10)
    BIRTH_PLACES = (
        ("BARCELONA", "Barcelona"),
        ("CATALUNYA", "Catalunya"),
        ("ESPANYA", "Espanya"),
        ("OTHER", "Altre")
    )
    birth_place = models.TextField("Lloc de naixement", blank=True, null=True, choices=BIRTH_PLACES)
    birthdate = models.DateField("Data de naixement", blank=True, null=True)
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, null=True, blank=True)
    DISTRICTS = (
        ('CV', 'Ciutat Vella'),
        ('EX', 'Eixample'),
        ('HG', 'Horta-Guinardó'),
        ('LC', 'Les Corts'),
        ('NB', 'Nou Barris'),
        ('SA', 'Sant Andreu'),
        ('SM', 'Sant Martí'),
        ('ST', 'Sants-Montjuïc'),
        ('SS', 'Sarrià-Sant Gervasi'),
        ('GR', 'Gràcia')
    )
    residence_district = models.TextField("Barri", blank=True, null=True, choices=DISTRICTS)
    address = models.CharField("Adreça", max_length=250, blank=True, null=True)
    phone_number = models.CharField("Telèfon", max_length=25, blank=True, null=True)
    STUDY_LEVELS = (
        ('MASTER', 'Màster / Postgrau'),
        ('HIGH_SCHOOL', 'Secundària'),
        ('WITHOUT_STUDIES', 'Sense estudis'),
        ('FP', 'Formació professional'),
        ('UNIVERSITY', 'Estudis universitaris'),
        ('ELEMENTARY_SCHOOL', 'Primària')
    )
    educational_level = models.TextField("Nivell d'estudis", blank=True, null=True, choices=STUDY_LEVELS)
    EMPLOYMENT_OPTIONS = (
        ('SELF_EMPLOYED', 'En actiu per compte propi'),
        ('UNEMPLOYMENT_BENEFIT_RECEIVER', 'Perceptora de prestacions socials'),
        ('UNEMPLOYMENT_BENEFIT_REQUESTED', "Demandant d'ocupació"),
        ('EMPLOYED_WORKER', 'En actiu per compte aliè')
    )
    employment_situation = models.TextField("Situació laboral", blank=True, null=True, choices=EMPLOYMENT_OPTIONS)
    DISCOVERED_US_OPTIONS = (
        ('INTERNET', 'Per internet i xarxes socials'),
        ('FRIEND', "A través d'un conegut"),
        ('PREVIOUS_ACTIVITY', "Per una activitat de Coòpolis"),
        ('OTHER', 'Altres')
    )
    discovered_us = models.TextField("Com ens has conegut", blank=True, null=True, choices=DISCOVERED_US_OPTIONS)
    cooperativism_knowledge = models.TextField("Coneixements previs",
                                               help_text="Tens coneixements / formació / experiència en "
                                                         "cooperativisme? Quina? Cursos realitzats?",
                                               blank=True, null=True)

    @property
    def project(self):
        try:
            r_stage = ProjectStage.objects.filter(involved_partners__id=self.id)[0:1].get()
            return r_stage.project
        except ProjectStage.DoesNotExist:
            return None

    def get_full_name(self):
        name = self.first_name
        if self.last_name:
            name = name + " " + self.last_name
        if self.surname2:
            name = name + " " + self.surname2
        return name

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()


class ProjectStageType(models.Model):
    class Meta:
        verbose_name = "tipus d'acompanyament"
        verbose_name_plural = "tipus d'acompanyaments"
        ordering = ["name"]

    name = models.CharField("nom", unique=True, max_length=100)

    def __str__(self):
        return self.name


class ProjectStage(models.Model):
    class Meta:
        verbose_name = "acompanyament"
        verbose_name_plural = "acompanyaments"
        ordering = ["-date_start"]

    DEFAULT_STAGE_TYPE = 1

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="acompanyament")
    stage_type = models.ForeignKey(ProjectStageType, verbose_name="tipus d'acompanyament", default=DEFAULT_STAGE_TYPE,
                                   on_delete=models.SET_DEFAULT)
    subsidy_period = models.CharField("convocatòria", blank=True, null=True, max_length=4, default=2019,
                                      choices=settings.SUBSIDY_PERIOD_OPTIONS)
    date_start = models.DateField("data d'inici", null=True, blank=True, default=datetime.date.today)
    date_end = models.DateField("data de finalització", null=True, blank=True)
    follow_up = models.TextField("seguiment", null=True, blank=True)
    axis = models.CharField("eix", help_text="Eix de la convocatòria on es justificarà.", choices=settings.AXIS_OPTIONS,
                            null=True, blank=True, max_length=1)
    organizer = models.CharField("qui ho fa", choices=settings.ORGANIZER_OTIONS, max_length=2, null=True, blank=True)
    stage_responsible = models.ForeignKey(
        "User", verbose_name="persona responsable", blank=True, null=True, on_delete=models.SET_NULL,
        related_name='stage_responsible', help_text="Persona de l'equip al càrrec de l'acompanyament. Per aparèixer "
        "al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.")
    scanned_signatures = models.FileField("document amb signatures", blank=True, null=True,
                                          upload_to=stage_signatures_upload_path, max_length=250)
    involved_partners = models.ManyToManyField(User, verbose_name="persones involucrades", blank=True,
                                               related_name='stage_involved_partners')

    def __str__(self):
        return str(self.project)
