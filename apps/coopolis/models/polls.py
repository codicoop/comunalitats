from django.db import models


class ActivityPoll(models.Model):
    class Meta:
        verbose_name = "enquesta de valoració"
        verbose_name_plural = "enquestes de valoració"

    # Organització
    duration = models.PositiveSmallIntegerField("la durada ha estat l'adequada?")
    hours = models.PositiveSmallIntegerField("els horaris han estat adequats?")
    information = models.PositiveSmallIntegerField("Informació necessària per fer l'activitat")
    on_schedule = models.PositiveSmallIntegerField("S'han complert les dates, horaris, etc...")
    included_resources = models.PositiveSmallIntegerField("Materials de suport facilitats")
    space_adequation = models.PositiveSmallIntegerField("Els espais han estat adequats (sales,aules...) ")

    # Continguts
    contents = models.PositiveSmallIntegerField("Els continguts han estat adequats")

    # Metodologia
    methodology_fulfilled_objectives = models.PositiveSmallIntegerField(
        "La metodologia ha estat coherent amb els objectius "
    )
    methodology_better_results = models.PositiveSmallIntegerField("La metodologia ha permès obtenir millors resultats")

    # Valoració de la persona formadora
    teacher_has_knowledge = models.PositiveSmallIntegerField("Ha mostrat coneixements i experiència sobre el tema?")
    teacher_resolved_doubts = models.PositiveSmallIntegerField(
        "Ha aconseguit resoldre els problemes i dubtes que s’ha plantejat?"
    )

    # Utilitat del curs
    expectations_satisfied = models.PositiveSmallIntegerField("Ha satisfet les meves expectatives")

    # Valoració global
    general_satisfaction = models.PositiveSmallIntegerField("Grau de satisfacció general")
    also_interested_in = models.TextField("De quins altres temes t'interessaria rebre formació?")
    comments = models.TextField("Vols comentar alguna cosa més?")
