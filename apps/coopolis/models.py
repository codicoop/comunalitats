from cc_users.models import BaseUser
from django.db import models


class User(BaseUser):
    class Meta:
        verbose_name_plural = "Usuaris"

    surname2 = models.TextField("Segon cognom", blank=True, null=True)
    id_number = models.TextField("DNI", blank=True, null=True)
    GENDERS = (
        'Altre',
        'Dona',
        'Home'
    )
    BIRTH_PLACES = (
        'Barcelona',
        'Catalunya',
        'Espanya',
        'Altres'
    )
    gender = models.TextField("Gènere", blank=True, null=True, choices=GENDERS)
    birthdate = models.DateField("Data de naixement", blank=True, null=True)
    birth_place = models.TextField("Lloc de naixement", blank=True, null=True, choices=BIRTH_PLACES)
    # TODO: Populate the dropdown with cities of Catalunya
    residence_town = models.TextField("Municipi de residència", blank=True, null=True,
                                      help_text="PENDING TO IMPORT IT FROM THE WORDPRESS DATABASE!!")
    DISTRICTS = (
        'Ciutat Vella',
        'Eixample',
        'Horta-Guinardó',
        'Les Corts',
        'Nou Barris',
        'Sant Andreu',
        'Sant Martí',
        'Sants-Montjuïc',
        'Sarrià-Sant Gervasi',
        'Gràcia'
    )
    residence_district = models.TextField("DNI", blank=True, null=True, choices=DISTRICTS)
    disability = models.BooleanField("Discapacitat")
    family_in_charge = models.BooleanField("Responsabilitats familiars")
    social_exclusion_risk = models.BooleanField("Risc d'exclusió social")
    phone_number = models.TextField("Telèfon", blank=True, null=True)
    STUDY_LEVELS = (
        'Màster / Postgrau',
        'Secundària',
        'Sense estudis',
        'Formació professional',
        'Estudis universitaris',
        'Primària'
    )
    educational_level = models.TextField("Nivell d'estudis", blank=True, null=True, choices=STUDY_LEVELS)
    EMPLOYMENT_OPTIONS = (
        'En actiu per compte propi',
        'Perceptora de prestacions socials',
        "Demandant d'ocupació",
        'En actiu per compte aliè'
    )
    employment_situation = models.TextField("Situació laboral", blank=True, null=True, choices=EMPLOYMENT_OPTIONS)
    DISCOVERED_US_OPTIONS = (
        'Per internet i xarxes socials',
        "A través d'un conegut",
        "Per una activitat de Coòpolis",
        'Altres'
    )
    discovered_us = models.TextField("Com ens has conegut", blank=True, null=True, choices=DISCOVERED_US_OPTIONS)

    @property
    def full_name(self):
        return self.get_full_name() if self.get_full_name() else self.username


class Project(models.Model):
    class Meta:
        verbose_name_plural = "Projectes"

    SECTORS = (
        ('A', 'Altres'),
        ('C', 'Comunicació i tecnologia'),
        ('F', 'Finances'),
        ('O', 'Oci'),
        ('H', 'Habitatge'),
        ('L', 'Logística'),
        ('E', 'Educació'),
        ('C', 'Cultura'),
        ('S', 'Assessorament')
    )
    name = models.CharField("Nom", max_length=200, blank=False, unique=True)
    sector = models.CharField(max_length=2, choices=SECTORS)
    web = models.CharField("Web", max_length=200, blank=True)
    mail = models.EmailField("Correu electrònic")
    phone = models.CharField("Telèfon", max_length=25)
    members = models.ManyToManyField(User, blank=True, related_name='projects')

    def __str__(self):
        return self.name
