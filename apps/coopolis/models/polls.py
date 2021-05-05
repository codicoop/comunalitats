from django.db import models


class ActivityPoll(models.Model):
    class Meta:
        verbose_name = "enquesta de valoració"
        verbose_name_plural = "enquestes de valoració"

    activity = models.ForeignKey(
        'cc_courses.Activity', on_delete=models.CASCADE, related_name="polls")
    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)

    # Organització
    duration = models.PositiveSmallIntegerField(
        "la durada ha estat l'adequada?", null=True, blank=True)
    hours = models.PositiveSmallIntegerField(
        "els horaris han estat adequats?", null=True, blank=True)
    information = models.PositiveSmallIntegerField(
        "Informació necessària per fer l'activitat", null=True, blank=True)
    on_schedule = models.PositiveSmallIntegerField(
        "S'han complert les dates, horaris, etc...", null=True, blank=True)
    included_resources = models.PositiveSmallIntegerField(
        "Materials de suport facilitats", null=True, blank=True)
    space_adequation = models.PositiveSmallIntegerField(
        "Els espais han estat adequats (sales, aules, plataforma digital...) ",
        null=True, blank=True
    )

    # Continguts
    contents = models.PositiveSmallIntegerField(
        "Els continguts han estat adequats", null=True, blank=True)

    # Metodologia
    methodology_fulfilled_objectives = models.PositiveSmallIntegerField(
        "La metodologia ha estat coherent amb els objectius ", null=True,
        blank=True
    )
    methodology_better_results = models.PositiveSmallIntegerField(
        "La metodologia ha permès obtenir millors resultats", null=True,
        blank=True
    )
    participation_system = models.PositiveSmallIntegerField(
        "el sistema de participació i resolució de dubtes ha estat adequat?",
        null=True, blank=True
    )

    # Valoració de la persona formadora
    teacher_has_knowledge = models.PositiveSmallIntegerField(
        "Ha mostrat coneixements i experiència sobre el tema?",
        null=True, blank=True
    )
    teacher_resolved_doubts = models.PositiveSmallIntegerField(
        "Ha aconseguit resoldre els problemes i dubtes que s’ha plantejat?",
        null=True, blank=True
    )
    teacher_has_communication_skills = models.PositiveSmallIntegerField(
        "el professional ha mostrat competències comunicatives?", null=True,
        blank=True
    )

    # Utilitat del curs
    expectations_satisfied = models.PositiveSmallIntegerField(
        "Ha satisfet les meves expectatives", null=True, blank=True)
    adquired_new_tools = models.PositiveSmallIntegerField(
        "He incorporat eines per aplicar a nous projectes", null=True,
        blank=True)
    met_new_people = models.NullBooleanField(
        "M'ha permès conèixer persones afins")
    wanted_start_cooperative = models.NullBooleanField(
        "Abans del curs, teníeu ganes/necessitats d'engegar algun projecte "
        "cooperatiu"
    )
    wants_start_cooperative_now = models.NullBooleanField("I després?")

    # Valoració global
    general_satisfaction = models.PositiveSmallIntegerField(
        "Grau de satisfacció general", null=True, blank=True)
    also_interested_in = models.TextField(
        "De quins altres temes t'interessaria rebre formació?", null=True,
        blank=True)
    heard_about_it = models.TextField(
        "com us heu assabentat d'aquesta activitat?", null=True, blank=True)
    comments = models.TextField(
        "Vols comentar alguna cosa més?", null=True, blank=True)

    def __str__(self):
        created = self.created.strftime('%d-%m-%Y')
        return f"Enquesta de {self.activity} del {created}"
