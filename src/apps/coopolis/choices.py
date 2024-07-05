from django.db import models


class ServicesChoices(models.IntegerChoices):
    """
    EN CAS QUE S'HAGI DE SEGUIR AFEGINT OPCIONS DIFERENTS EN NOVES
    CONVOCATÒRIES:
    Crec que caldrà migrar cap a un sistema de models en el que servei i
    subservei pengin de Convocatòria.
    Veure comentaris de la view get_subsidy_period.
    """

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
    # Nomenclatura serveis | HORES ITERACIONS 2023
    F = 60, "A) Serveis d'anàlisis i prospectiva"
    G = 70, ("B) Servei de formació i difusió per a l'activisme al barri/espai "
             "urbà adreçat a entitats i persones")
    H = 80, (
        "C) Servei de foment a projectes d'ajuda mútua, "
        "d'intercooperació i de cooperació entre els bens "
        "comuns urbans i la ciutadania"
    )
    J = 90, (
        "D) Servei d’acompanyament a la creació i "
        "a la consolidació de projectes d'ajuda mútua"
    )

    def get_sub_services(self):
        range_start = self.value * 10
        range_end = range_start + 99
        return [
            member
            for member in SubServicesChoices
            if member in range(range_start, range_end + 1)
        ]


class SubServicesChoices(models.IntegerChoices):
    """
    EN CAS QUE S'HAGI DE SEGUIR AFEGINT OPCIONS DIFERENTS EN NOVES
    CONVOCATÒRIES:
    Crec que caldrà migrar cap a un sistema de models en el que servei i
    subservei pengin de Convocatòria.
    Veure comentaris de la view get_subsidy_period.
    """

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
        "B.1) Campanya de comunicació i difusió a col.lectius d'especial "
        "atenció"
    )
    B2 = 202, "B.2) Elaboració de material especific i difusió dels materials"
    B3 = 203, (
        "B.3) Activitats anuals de dinamització  i activació de "
        "l'autoorganització "
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

    # Nomenclatura subserveis | HORES ITERACIONS 2023
    # A) Servei anàlisi i prospectiva.
    F1 = 601, ("A.1) Diagnosi i/o avaluació de necessitats de forma participada "
               "a nivell general i/o sectorial")
    F2 = 602, ("A.2) Identificació i visualització de béns comuns urbans i "
               "altres iniciatives de suport mutu, activisme i ESS del territori")
    F3 = 603, ("A.3) Elaboració de materials i suports de difusió de bones "
               "pràctiques de suport mutu, activisme i ESS del territori")
    F4 = 604, "A.4) Enxarxament territorial i de barri"
    F5 = 605, ("A.5) Articulació i posada en funcionament de l’Assemblea, així "
               "com d’altres espais de governança democràtica i inclusiva de "
               "la Comunalitat")

    # B) Servei de formació i difusió per a l'activisme al barri/espai urbà
    # adreçat a entitats i persones
    G1 = 701, "B.1) Campanya de comunicació a col·lectius d'especial atenció"
    G2 = 702, ("B.2) Dinamització per donar a conèixer projectes d’ajuda mútua, "
               "l’autogestió, ESS i cooperativisme, al teixit associatiu i a "
               "les empreses")
    G3 = 703, ("B.3) Organització de jornades i assistència a accions directes "
               "de la comunalitat per visibilitzar experiències")
    G4 = 704, ("B.4) Generació d’espais de trobada i d'intercanvi d’experiències"
               " i col·laboració en iniciatives conjuntes entre actors i "
               "sectors diversos.")
    G5 = 705, ("B.5) Realització de formacions i/o divulgació de coneixement "
               "compartit entorn el suport mutu, l’activisme, els béns comuns "
               "i l’ESS")

    # C) Servei de foment a projectes d'ajuda mútua, d'intercooperació i de
    # cooperació entre els bens comuns urbans i la ciutadania.
    H1 = 801, ("C.1) Orientació a persones, empreses i entitats per la creació "
               "d’activitats econòmiques i iniciatives empresarials de l’ESS")
    H2 = 802, ("C.2) Generació d’aliances entre professionals per promoure "
               "l'ocupabilitat digne a través de la intercooperació")
    H3 = 803, ("C.3) Creació o consolidació dinàmiques de col·laboració i"
               " aliances entre diferents agents econòmics de forma "
               "democràtica i inclusiva")
    H4 = 804, ("C.4) Organització de sessions per al disseny d'estratègies "
               "vinculades a l'autoorganització col·lectiva, xarxes de suport "
               "mutu, intercooperació")
    H5 = 805, ("C.5) Activitats per a la creació d’aliances i l’accés a l’ús "
               "comunal d’infraestructures i recursos")

    # D) Servei d’acompanyament a la creació i a la consolidació de projectes
    # d'ajuda mútua.
    J1 = 901, ("D.1) Acompanyament a projectes veïnals, socials i/o comunitaris "
               "per a la resolució de necessitats col·lectives")
    J2 = 902, ("D.2) Generació de nous projectes d'intercooperació o ajuda "
               "mútua dirigides i realitzades amb col·lectius específics")


class ProjectSectorChoices(models.IntegerChoices):
    A = 10, "Agricultura i ramaderia",
    B = 20, "Alimentació i consum",
    C = 30, "Atenció a les persones i cures (criança, col·lectius vulnerables...)",
    D = 40, "Comerç (just, proximitat, etc.)",
    E = 50, "Cultura i oci (lleure, esport, esdeveniments...)",
    F = 60, "Economia circular (reciclatge, recuperació i reutilització de residus)",
    G = 70, "Educació / Formació",
    H = 80, "Feminismes LGTBIQ+",
    J = 90, "Finançament i assegurances (micromecenatge, finances ètiques, ....)",
    K = 100, "Gestió i conservació de l'espai natural (gestió de residus,",
    L = 110, "Hosteleria i restauració",
    M = 120, "Industria",
    N = 130, "Joventut",
    P = 140, "Logística i mobilitat (transports, bancs de recursos, emmagatzematge...)",
    Q = 150, "Màrqueting i comunicació (xarxes, audiovisual, arts gràfiques, disseny...)",
    R = 160, "Ruralitats (despoblament, relleu,...)",
    S = 170, "Salut (mental, sexualitat, ...)",
    T = 180, "Serveis d'assessoria i gestoria",
    U = 190, "Tecnologies i innovació",
    V = 200, "Transició energètica / recursos naturals",
    W = 210, "Turisme (rural, sostenible,...)",
    X = 220, "Urbanisme i habitatge (arquitectura, rehabilitació, masoveria, ...)",

class TypesChoices(models.IntegerChoices):
    A = 1, "Acompanyament",
    B = 2, "Acte",
    C = 3, "Cartografia /mapeig",
    D = 4, "Cicle",
    E = 5, "Entrevista",
    F = 6, "Exposició",
    G = 7, "Festival",
    H = 8, "Fira",
    J = 9, "Inauguració",
    K = 10, "Jornada",
    L = 11, "Premi",
    M = 12, "Presentació",
    N = 13, "Publicació",
    P = 14, "Punt informació",
    Q = 15, "Reunió",
    R = 16, "Sessió formativa/ informativa",
    S = 17, "Taller",
    T = 18, "Trobada",
    U = 19, "Trobades assemblea",
    V = 20, "Visita",
    W = 21, "Xerrada",

class CommunalityRoleChoices(models.IntegerChoices):
    A = 1, "Participant / Assistent (rol passiu)",
    B = 2, "Organitzador / Col·laborador (rol actiu)",


class NetworkingChoices(models.IntegerChoices):
    A = 1, "Individual",
    B = 2, "Conjunta",
