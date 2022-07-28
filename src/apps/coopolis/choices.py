import sys

from django.conf import settings
from django.db import models


class ServicesChoices(models.IntegerChoices):
    __empty__ = "Cap"
    A = 10, "A) Serveis d'anàlisis i prospectiva"
    B = 20, "B) Servei de formació i difusió per a l'activisme"
    C = 30, (
        "C) Servei de formació per a la creació i l'establiment de projectes "
        "d'ajuda mútua"
    )
    D = 40, (
        "D) Servei per a la creació i consolidació de projectes d'ajuda mútua, "
        "d'intercooperació i de cooperació entre els bens comuns urbans i la "
        "ciutadania"
    )
    E = 50, "E) Punt de trobada i d'informació de comunalitat urbana"

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

    # A. Serveis d'anàlisis i prospectiva
    A1 = 101, (
        "A.1) Articulació i posada en funcionament de l'Assemblea de la "
        "Comunalitat"
    )
    A2 = 102, (
        "A.2) Identificació i incorporació dels béns comuns urbans, de les "
        "organitzacions, els col.lectius i els representants"
    )
    A3 = 103, (
        "A.3) Creació o manteniment i difusió d'un recurs/ eina per visualitzar "
        "béns comuns i projectes d'ajuda mútua assolits. "
    )
    A4 = 104, (
        "A.4) Elaboració d'un catàleg d'exemples de bones pràctiques d'ajuda mútua "
        "i ESS. Identificar i elaborar fitxes de bones pràctiques i iniciatives"
    )
    A5 = 105, (
        "A.5) Organització de jornades i accions directes a la comunalitat per "
        "visualitzar experiències; fires,actes, presència als mitjans de "
        "comunicació. "
    )
    A6 = 106, (
        "A.6) Organització logística i metodològica de jornades pròpies per "
        "presentar bones pràctiques, parlar de temes sectorials o d'interés "
        "per el territori"
    )
    A7 = 107, (
        "A.7) Participació o colaboració a actes, jornades, fires, publicacions "
        "amb l'objectiu de presentar el programa, visibilitzar experiències,"
        "organitzar tallers, publicar notes de premsa o articles opinió"
    )
    A8 = 108, (
        "A.8) Altres accions dins el servei d'anàlisi i prospectiva "
    )

    # B. Servei de formació i difusió per a l'activisme
    B1 = 201, (
        "Campanya de comunicació i difusió a col.lectius d'especial atenció"
    )
    B2 = 202, "Elaboració de material especific i difusió dels materials"
    B3 = 203, (
        "Activitats anuals de dinamització  i activació de l'autoorganització "
        "col.lectiva per  a la generació de projectes"
    )
    B4 = 204, (
        "B.4)Tallers adreçats preferentment als joves o a la ciutadania de la "
        "comunalitat."
    )
    B5 = 205, (
        "B.5) Altres accions dins el servei de formació i difusió per a "
        "l'activisme al barri/espai urbà"
    )

    # C. Servei de formació per a la creació i l'establiment de projectes
    # d'ajuda mútua
    C1 = 301, (
        "C.1) Activitats formatives i informatives per a la creció d'aliances "
    )
    C2 = 302, (
        "C.2) Organització de formació bàsica o dinamització destinades "
        "a persones o entitats interessades en la fórmula de colaboració, "
        "ajuda mutua o intercooperació"
    )
    C3 = 303, (
        "C.3) Organització de sessions col.lectives i individuals per al "
        "disseny d'estratègies vinculades a l'autoorganització i "
        "intercooperació"
    )
    C4 = 304, (
        "C.4) Activitats destinades a fomentar la col.laboració entre empreses "
        "de l'economia social i cooperativa del territori"
    )
    C5 = 305, (
        "C.5) Organització i acompanyament a les empreses/entitats "
        "participants en la primera fase de coordinació del projecte. "
    )
    C6 = 306, (
        "C.6) Elaboració i difusió de materials destinat a empreses, "
        "associassions i entitats sobre ajuda mútua i ESS"
    )
    C7 = 307, (
        "C.7) Tallers de sensibilització/dinamització destinats al teixit "
        "associatiu i a les empreses per donar a conèixer projectes "
    )
    C8 = 308, (
        "C.8) Tallers de sensibilització/dinamització adreçats a professionals "
        "que s'agrupin de manera conjunta"
    )
    C9 = 309, (
        "C.9) Altres accions dins el servei de formació per a la creació i "
        "establiment de projectes d'ajuda"
    )

    # 4. Servei per a la creació i consolidació de projectes d'ajuda mútua,
    # d'intercooperació i de cooperació entre els bens comuns urbans i la
    # ciutadania
    D1 = 401, (
        "D.1) Creació d'espais d'intercooperació dins els territoris de "
        "referència per la generació de nous models econòmics"
    )
    D2 = 402, (
        "D.2) Incorporació d'empreses, cooperatives i entitats ESS en els "
        "béns comuns urbans"
    )
    D3 = 403, (
        "D.3) Activitats de treball en xarxa amb altres comunalitats urbanes "
        "del programa "
    )
    D4 = 404, (
        "D.4) Altres accions dins el servei per a la creació i "
              "consolidació de projectes d'ajuda mútua"
    )

    # 5. Punt de trobada i d'informació de comunalitat urbana
    E1 = 501, "E.1) Atenció als usuaris a l'espai físic de referència"
    E2 = 502, "E.2) Difusió del punt d'informació"
