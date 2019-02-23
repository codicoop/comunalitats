from cc_users.models import BaseUser
from django.db import models
from uuid import uuid4
from cc_users.managers import CCUserManager
from simple_history.models import HistoricalRecords


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
    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
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
        ('COOPERATIVISM_EDUCATION', 'Formació en cooperativimse'),
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
    project_responsible = models.ForeignKey("User", verbose_name="Persona responsable", blank=True, null=True,
                                            on_delete=models.SET_NULL, related_name='project_responsible',
                                            help_text="Persona de l'equip al càrrec de l'acompanyament. Per aparèixer "
                                            "al desplegable, cal que la persona tingui activada la opció 'Membre del "
                                            "personal'.")
    number_people = models.IntegerField("Número de persones", blank=True, null=True)
    registration_date = models.DateField("Data de registre", blank=True, null=True)
    cif = models.CharField("NIF", max_length=11, blank=True, null=True)
    subsidy_period = models.TextField("Convocatòria", blank=True, null=True,
                                      choices=(("2018", "2018"), ("2019", "2019")))
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
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class User(BaseUser):
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Persones"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CCUserManager()

    username = models.CharField(unique=False, max_length=150, verbose_name="Nom d'usuari/a")
    surname2 = models.CharField("Segon cognom", max_length=50, blank=True, null=True)
    id_number = models.CharField("DNI o NIE", max_length=11)
    GENDERS = (
        ('A', 'Altre'),
        ('D', 'Dona'),
        ('H', 'Home')
    )
    BIRTH_PLACES = (
        ("B", "Barcelona"),
        ("C", "Catalunya"),
        ("E", "Espanya"),
        ("A", "Altre")
    )
    gender = models.TextField("Gènere", blank=True, null=True, choices=GENDERS)
    birthdate = models.DateField("Data de naixement", blank=True, null=True)
    birth_place = models.TextField("Lloc de naixement", blank=True, null=True, choices=BIRTH_PLACES)
    CITIES = (
        ('78', 'Badalona'),
        ('79', 'Badia del Vallès'),
        ('89', 'Barberà del vallès'),
        ('90', 'Barcelona'),
        ('96', 'Begues'),
        ('200', 'Castellbisbal'),
        ('203', 'Castelldefels'),
        ('226', 'Cerdanyola del Vallès'),
        ('227', 'Cervelló'),
        ('246', 'Corbera de Llobregat'),
        ('250', 'Cornellà de Llobregat'),
        ('527', 'El Papiol'),
        ('581', 'El Prat de Llobregat'),
        ('269', 'Esplugues de Llobregat'),
        ('323', 'Gavà'),
        ('356', "L'Hospitalet de Llobregat"),
        ('523', 'La Palma de Cervelló'),
        ('441', 'Molins de Rei'),
        ('452', 'Montcada i Reixac '),
        ('459', 'Montgat'),
        ('522', 'Pallejà'),
        ('621', 'Ripollet'),
        ('653', 'Sant Adrià de Besòs'),
        ('655', 'Sant Andreu de la barca'),
        ('661', 'Sant Boi de Llobregat'),
        ('666', 'Sant Climent de Llobregat'),
        ('668', 'Sant Cugat del Valles'),
        ('676', 'Sant Feliu de Llobregat'),
        ('695', 'Sant Joan Despí'),
        ('702', 'Sant Just Desvern'),
        ('738', 'Sant Vicenç dels Horts'),
        ('743', 'Santa Coloma de Gramenet'),
        ('818', 'Tiana'),
        ('841', 'Torrelles de Llobregat'),
        ('899', 'Viladencans'),
        ('0', 'Altres')
    )
    residence_town = models.CharField("Municipi de residència", max_length=150, blank=True, null=True, choices=CITIES)
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
    address = models.CharField("Adreça", max_length=50, blank=True, null=True)
    phone_number = models.CharField("Telèfon", max_length=25, blank=True, null=True)
    STUDY_LEVELS = (
        ('MP', 'Màster / Postgrau'),
        ('SD', 'Secundària'),
        ('SE', 'Sense estudis'),
        ('FP', 'Formació professional'),
        ('FU', 'Estudis universitaris'),
        ('PR', 'Primària')
    )
    educational_level = models.TextField("Nivell d'estudis", blank=True, null=True, choices=STUDY_LEVELS)
    EMPLOYMENT_OPTIONS = (
        ('AP', 'En actiu per compte propi'),
        ('PS', 'Perceptora de prestacions socials'),
        ('DO', "Demandant d'ocupació"),
        ('AA', 'En actiu per compte aliè')
    )
    employment_situation = models.TextField("Situació laboral", blank=True, null=True, choices=EMPLOYMENT_OPTIONS)
    DISCOVERED_US_OPTIONS = (
        ('IN', 'Per internet i xarxes socials'),
        ('CO', "A través d'un conegut"),
        ('AC', "Per una activitat de Coòpolis"),
        ('AL', 'Altres')
    )
    discovered_us = models.TextField("Com ens has conegut", blank=True, null=True, choices=DISCOVERED_US_OPTIONS)
    cooperativism_knowledge = models.TextField("Coneixements previs",
                                               help_text="Tens coneixements / formació / experiència en "
                                                         "cooperativisme? Quina? Cursos realitzats?",
                                               blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Projecte")
    history = HistoricalRecords()

    @property
    def full_name(self):
        return self.get_full_name() if self.get_full_name() else self.username
