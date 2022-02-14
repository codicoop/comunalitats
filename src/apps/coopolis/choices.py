import sys

from django.conf import settings
from django.db import models


class ServicesChoices(models.IntegerChoices):
    __empty__ = "Cap"
    MAP_DIAGNOSI = 10, "Servei de mapatge i diagnosi"
    DIV_SENS_GEN_CONEIXEMENT = 20, ("Servei de Divulgació, Sensibilització i "
    "Generació de Coneixement.")
    FORM_PROM_CREA_CONS = 30, ("Servei de Formació per a la promoció, creació "
    "i consolidació de cooperatives i projectes de l'ESS.")
    ACOM_CREA_CONS = 40, ("Servei d'Acompanyament per la creació i "
    "consolidació de cooperatives i projectes de l'ESS.")
    INTERCOOP_XARXA_TERRITORI = 50, ("Servei de Facilitació de la "
    "Intercooperació, treball en xarxa i dinamització territorial.")
    PUNT_INFO = 60, "Punt d'informació sobre l'ESS."


class CirclesChoices(models.IntegerChoices):
    __empty__ = "Cap"
    CERCLE0 = 0, "Ateneu"
    CERCLE1 = 1, "Cercle 1"
    CERCLE2 = 2, "Cercle 2"
    CERCLE3 = 3, "Cercle 3"
    CERCLE4 = 4, "Cercle 4"
    CERCLE5 = 5, "Cercle 5"

    @classmethod
    def choices_named(cls):
        if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
            return cls.choices
        choices = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        for member in cls:
            if settings.CIRCLE_NAMES[member.value]:
                label = f"{member.label}: {settings.CIRCLE_NAMES[member.value]}"
            else:
                label = member.label
            choices.append((member.value, label))
        return choices
