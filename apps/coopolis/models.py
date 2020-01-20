from django.db import models
from django.conf import settings
from uuid import uuid4
import datetime
from django.core.validators import ValidationError

from cc_users.models import BaseUser
from cc_courses.models import Entity
from cc_users.managers import CCUserManager
from coopolis.helpers import get_subaxis_choices
from dataexports.models import SubsidyPeriod
from apps.coopolis.storage_backends import PrivateMediaStorage


class Town(models.Model):
    class Meta:
        verbose_name = "població"
        verbose_name_plural = "poblacions"

    name = models.CharField("nom", max_length=250)

    def __str__(self):
        return self.name


class Derivation(models.Model):
    class Meta:
        verbose_name = "derivació"
        verbose_name_plural = "derivacions"

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
        ('CU', 'Cultura'),
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
    estatuts = models.FileField("estatuts", blank=True, null=True, storage=PrivateMediaStorage(), max_length=250)
    viability = models.FileField("pla de viabilitat", blank=True, null=True, storage=PrivateMediaStorage(),
                                 max_length=250)
    sostenibility = models.FileField("pla de sostenibilitat", blank=True, null=True, storage=PrivateMediaStorage(),
                                     max_length=250)
    derivation = models.ForeignKey(Derivation, verbose_name="derivat", on_delete=models.SET_NULL, blank=True, null=True)
    derivation_date = models.DateField("data de derivació", blank=True, null=True)


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

    @property
    def stages_list(self):
        if not self.stages or self.stages.count() < 1:
            return None
        stages = []
        for stage in self.stages.all():
            stages.append(stage.get_stage_type_display())
        stages.sort()
        return "; ".join(stages)

    @property
    def last_stage_responsible(self):
        if not self.stages or self.stages.count() < 1:
            return None
        return self.stages.all()[0].stage_responsible
    last_stage_responsible.fget.short_description = "Últim acompanyament"

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
    id_number = models.CharField("DNI/NIE/Passaport", null=True, max_length=11)
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
        ('PREVIOUS_ACTIVITY', "Per una activitat de l'ateneu"),
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

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="projecte acompanyat",
                                related_name="stages")
    STAGE_TYPE_OPTIONS = (
        ('1', "00 Nova creació - acollida"),
        ('2', "01 Nova creació - procés"),
        ('6', "02 Nova creació - constitució"),
        ('7', "03 Consolidació - 1a acollida"),
        ('8', "04 Consolidació - acompanyament")
    )
    stage_type = models.CharField("tipus d'acompanyament", max_length=2, default=DEFAULT_STAGE_TYPE,
                                  choices=STAGE_TYPE_OPTIONS)
    subsidy_period = models.ForeignKey(SubsidyPeriod, null=True, on_delete=models.SET_NULL)
    date_start = models.DateField("data d'inici", null=True, blank=True, default=datetime.date.today)
    date_end = models.DateField("data de finalització", null=True, blank=True)
    follow_up = models.TextField("seguiment", null=True, blank=True)
    axis = models.CharField("eix", help_text="Eix de la convocatòria on es justificarà.", choices=settings.AXIS_OPTIONS,
                            null=True, blank=True, max_length=1)
    subaxis = models.CharField("sub-eix", help_text="Correspon a 'Tipus d'acció' a la justificació.",
                               null=True, blank=True, max_length=2, choices=get_subaxis_choices())
    organizer = models.ForeignKey(Entity, verbose_name="qui ho fa", default=None, null=True, blank=True,
                                  on_delete=models.SET_NULL)
    stage_responsible = models.ForeignKey(
        "User", verbose_name="persona responsable", blank=True, null=True, on_delete=models.SET_NULL,
        related_name='stage_responsible', help_text="Persona de l'equip al càrrec de l'acompanyament. Per aparèixer "
        "al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.")
    scanned_signatures = models.FileField(
        "fitxa de projectes (document amb signatures)", blank=True, null=True, storage=PrivateMediaStorage(),
        max_length=250)
    scanned_certificate = models.FileField(
        "certificat", blank=True, null=True, storage=PrivateMediaStorage(), max_length=250)
    hours = models.IntegerField(
        "número d'hores", help_text="Camp necessari per la justificació.", null=True, blank=True)
    involved_partners = models.ManyToManyField(
        User, verbose_name="persones involucrades", blank=True, related_name='stage_involved_partners',
        help_text="Persones que apareixeran a la justificació com a que han participat a l'acompanyament.")

    def clean(self):
        super().clean()
        if self.subaxis:
            if not self.axis:
                raise ValidationError({'axis': "Si selecciones un sub-eix, cal indicar també l'eix corresponent."})
            if self.axis not in self.subaxis:
                raise ValidationError({'subaxis': f"El sub-eix { self.subaxis } no pertany a l'eix { self.axis }."})

        if self.subsidy_period and self.date_end:
            if self.date_end < self.subsidy_period.date_start or self.date_end > self.subsidy_period.date_end:
                raise ValidationError({'date_end': "La data de finalització ha d'estar dins del període de la "
                                                   "convocatòria seleccionada."})

    def __str__(self):
        return f"{str(self.project)}: {self.get_stage_type_display()}"


class EmploymentInsertion(models.Model):
    class Meta:
        verbose_name = "inserció laboral"
        verbose_name_plural = "insercions laborals"
        ordering = ["-insertion_date"]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="projecte acompanyat",
                                related_name="employment_insertions")
    user = models.ForeignKey(User, verbose_name="persona", blank=True, null=True, on_delete=models.PROTECT)
    insertion_date = models.DateField("alta seguretat social")
    CONTRACT_TYPE_CHOICES = (
        ('autonom', "Autònom -RETA-"),
        ('general_cpropi', "Règim general - compte propi"),
        ('general_calie', "Règim general - compte aliè"),
    )
    contract_type = models.CharField("tipus de contracte", max_length=50, choices=CONTRACT_TYPE_CHOICES)
    DURATION_CHOICES = (
        ('indefinit', "Indefinit"),
        ('obraservei', "Obra i servei"),
        ('temporal', "Temporal"),
    )
    duration = models.CharField("durada", max_length=50, choices=DURATION_CHOICES)

    def __str__(self):
        return f"{ self.user.full_name }: { self.contract_type }"
