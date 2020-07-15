from django.db import models

from ..models import User


class ActivityPoll(models.Model):
    class Meta:
        verbose_name = "enquesta de valoració"
        verbose_name_plural = "enquestes de valoració"

    activity = models.ForeignKey('cc_courses.Activity', on_delete=models.CASCADE, related_name="polls")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)

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
    adquired_new_tools = models.PositiveSmallIntegerField("He incorporat eines per aplicar a nous projectes")
    met_new_people = models.NullBooleanField("M'ha permès conèixer persones afins")
    wanted_start_cooperative = models.NullBooleanField(
        "Abans del curs, teníeu ganes/necessitats d'engegar algun projecte cooperatiu"
    )
    wants_start_cooperative_now = models.NullBooleanField("I després?")

    # Valoració global
    general_satisfaction = models.PositiveSmallIntegerField("Grau de satisfacció general")
    also_interested_in = models.TextField("De quins altres temes t'interessaria rebre formació?")
    comments = models.TextField("Vols comentar alguna cosa més?")

    def __str__(self):
        return f"Enquesta de {self.activity} del {self.created.strftime('%d-%m-%Y')}"
