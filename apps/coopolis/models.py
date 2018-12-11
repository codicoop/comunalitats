from cc_users.models import BaseUser
from django.db import models


class User(BaseUser):
    class Meta:
        verbose_name_plural = "Usuaris"

    surname2 = models.CharField("Segon cognom", max_length=50, blank=True, null=True)
    id_number = models.CharField("DNI", max_length=11, blank=True, null=True)
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
    # TODO: Populate the dropdown with cities of Catalunya
    residence_town = models.CharField("Municipi de residència", max_length=150, blank=True, null=True,
                                      help_text="PENDING TO IMPORT IT FROM THE WORDPRESS DATABASE!!")
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
    residence_district = models.TextField("DNI", blank=True, null=True, choices=DISTRICTS)
    disability = models.BooleanField("Discapacitat", blank=True, null=True)
    family_in_charge = models.BooleanField("Responsabilitats familiars", blank=True, null=True)
    social_exclusion_risk = models.BooleanField("Risc d'exclusió social", blank=True, null=True)
    phone_number = models.TextField("Telèfon", max_length=25, blank=True, null=True)
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
    adreca_tipus_via = models.CharField("Tipus de via", max_length=50, blank=True, null=True)
    adreca_nom_via = models.CharField("Nom de la via", max_length=150, blank=True, null=True)
    adreca_numero = models.CharField("Número", max_length=50, blank=True, null=True)
    adreca_bloc = models.CharField("Bloc / Escala", max_length=50, blank=True, null=True)
    adreca_planta = models.CharField("Planta", max_length=50, blank=True, null=True)
    adreca_porta = models.CharField("Porta", max_length=50, blank=True, null=True)

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
