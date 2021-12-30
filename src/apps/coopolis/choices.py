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
