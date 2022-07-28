import sys

from django.conf import settings
from django.db import models


class ServicesChoices(models.IntegerChoices):
    __empty__ = "Cap"
    MAP_DIAGNOSI = 10, "Servei de mapatge i diagnosi"
    DIV_SENS_GEN_CONEIXEMENT = 20, (
        "Servei de Divulgació, Sensibilització i Generació de Coneixement."
    )
    FORM_PROM_CREA_CONS = 30, (
        "Servei de Formació per a la promoció, creació i consolidació de "
        "cooperatives i projectes de l'ESS."
    )
    ACOM_CREA_CONS = 40, (
        "Servei d'Acompanyament per la creació i "
        "consolidació de cooperatives i projectes de l'ESS."
    )
    INTERCOOP_XARXA_TERRITORI = 50, (
        "Servei de Facilitació de la "
        "Intercooperació, treball en xarxa i dinamització territorial."
    )
    PUNT_INFO = 60, "Punt d'informació sobre l'ESS."

    def get_sub_services(self):
        range_start = self.value * 10
        range_end = range_start + 99
        return [
            member
            for member in SubServicesChoices
            if member in range(range_start, range_end + 1)
        ]


class SubServicesChoices(models.IntegerChoices):
    __empty__ = "Cap"

    # 1. Servei de mapeig i diagnosi
    MAP_DIAGNOSI_TAULA = 101, (
        "Taula territorial per l'articulació conjunta de l'economia social amb "
        "els diversos actors."
    )
    MAP_DIAGNOSI_CATALEG = 102, "Elaboració d'un catàleg bones pràctiques."
    MAP_DIAGNOSI_ORGANITZACIO = 103, (
        "Organització de jornades per visibilitzar experiències, presència "
        "als mitjans de comunicació locals, assistència a fires, actes i "
        "premis, trobades sectorials, col·laboracions amb altres iniciatives."
    )
    MAP_DIAGNOSI_ALTRES = 199, (
        "Altres accions dins del servei de mapeig i diagnosi (si s'escau "
        "desenvolupeu a la memòria)"
    )

    # 2. Servei de divulgació, sensibilització i generació de coneixement
    DIV_SENS_GEN_CONEIXEMENT_CAMPANYA = 201, (
        "Campanya de Comunicació i difusió a col·lectius d'especial atenció. "
        "Materials específic de difusió sobre la fórmula cooperativa."
    )
    DIV_SENS_GEN_CONEIXEMENT_TALLERS = 202, (
        "Tallers dirigits a joves estudiants de cicles formatius "
        "presencials o virtuals ."
    )
    DIV_SENS_GEN_CONEIXEMENT_ACCIONS = 203, (
        "Accions per a la creació de diferents classes de cooperatives "
        "(concursos i tallers sensibilització)"
    )
    DIV_SENS_GEN_CONEIXEMENT_DIAGNOSI = 204, (
        "Diagnosi sobre les mancances i oportunitats socioeconòmiques i "
        "identificació de les empreses participants."
    )
    DIV_SENS_GEN_CONEIXEMENT_SESSIONS = 205, (
        "Sessions col·lectives i d'acompanyament expert individual."
    )
    DIV_SENS_GEN_CONEIXEMENT_ALTRES = 299, (
        "Altres accions dins del servei de "
        "divulgació, sensibilitzacio i generació de coneixement (si s'escau " 
        "desenvolupeu a la memòria)"
    )

    # 3. Servei de Formació per a la promoció, creació i consolidació de
    # cooperatives i projectes d'ESS
    FORM_PROM_CREA_CONS_ACTIVITATS = 301, "Activitats formatives i informatives."
    FORM_PROM_CREA_CONS_FORMACIO = 302, (
        "Tallers de formació bàsica a persones emprenedores interessades en la "
        "fòrmula cooperativa ."
    )
    FORM_PROM_CREA_CONS_SESSIONS = 303, "Sessions col·lectives"
    FORM_PROM_CREA_CONS_ACOMPANYAMENT = 304, "Acompanyament expert"
    FORM_PROM_CREA_CONS_SENSIBILITZACIO = 305, (
        "Tallers de sensibilització o dinamització adreçada al teixit "
        "associatiu, empreses o professionals."
    )
    FORM_PROM_CREA_CONS_ALTRES = 399, (
        "Altres accions dins del servei de formació (si s'escau desenvolupeu a "
        "la memòria)"
    )

    # 4. Servei d'acompanyament per a la creació i consolidació de cooperatives
    # i projectes d'ESS
    ACOM_CREA_CONS_CREACIO = 401, (
        "Assessorament a mida per a la creació de cooperatives i altres "
        "organitzacions d'ESS"
    )
    ACOM_CREA_CONS_CONSOLIDACIO = 402, (
        "Acompanyament a la consolidació i creixement de cooperatives existents"
    )
    ACOM_CREA_CONS_TRANSFORMACIO = 403, (
        "Acompanyament a la transformació d'empreses"
    )
    ACOM_CREA_CONS_CAMPANYA = 404, "Campanya de comunicació i difusió"
    ACOM_CREA_CONS_SENSIBILITZACIO = 405, (
        "Accions de sensibilització o dinamització"
    )
    ACOM_CREA_CONS_ALTRES = 499, (
        "Altres accions dins del servei d'acompanyament (si s'escau "
        "desenvolupeu a la memòria)"
    )

    # 5. Servei de facilitació de la intercooperació, treball en xarxa i
    # dinamització territorial
    INTERCOOP_XARXA_TERRITORI_INTERCOOPERACIO = 501, (
        "Generar espais d'intercooperació i treball en xarxa dins del "
        "territori, intercooperació local, creació d'espais i grups "
        "d'intercooperació"
    )
    INTERCOOP_XARXA_TERRITORI_INCORPORACIO = 502, (
        "Incorporació d'empreses a l'ateneu cooperatiu i assemblea"
    )
    INTERCOOP_XARXA_TERRITORI_TREBALL = 503, (
        "Treball en xarxa amb altres ateneus: assistir a reunions i col·laborar"
        " en iniciatives conjuntes."
    )
    INTERCOOP_XARXA_TERRITORI_ALTRES = 599, (
        "Altres accions dins del servei de facilitació (si s'escau "
        "desenvolupeu a la memòria)"
    )

    # 6. Punt d'informació sobre l'ESS
    PUNT_INFO_ESPAI = 601, (
        "Espai físic per proporcionar informació sobre ESS a diferents públics"
    )
    PUNT_INFO_DIFUSIO = 602, "Difusió del Punt o punts d'informació"
