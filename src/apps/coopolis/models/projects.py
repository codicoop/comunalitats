import datetime

from constance import config
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe
from django.utils.timezone import now
import tagulous.models

from apps.cc_courses.models import Entity, Organizer, Cofunding, StrategicLine
from apps.coopolis.choices import ServicesChoices, CirclesChoices
from apps.coopolis.helpers import get_subaxis_choices, get_subaxis_for_axis
from apps.coopolis.models import Town, User
from apps.coopolis.storage_backends import PrivateMediaStorage, PublicMediaStorage
from apps.dataexports.models import SubsidyPeriod


class Derivation(models.Model):
    class Meta:
        verbose_name = "derivació"
        verbose_name_plural = "derivacions"

    name = models.CharField("nom", max_length=250)

    def __str__(self):
        return self.name


class Project(models.Model):
    class Meta:
        verbose_name_plural = "projectes"
        verbose_name = "projecte"

    partners = models.ManyToManyField('User', verbose_name="sòcies",
                                      blank=True, related_name='projects')
    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    SECTORS = (
        ('A', 'Altres'),
        ('C', 'Comunicació i tecnologia'),
        ('F', 'Finances'),
        ('O', 'Oci'),
        ('H', 'Habitatge'),
        ('L', 'Logística'),
        ('E', 'Educació'),
        ('CU', 'Cultura'),
        ('S', 'Assessorament'),
        ('M', 'Alimentació'),
        ('U', 'Cures'),
        ('R', 'Roba')
    )
    sector = models.CharField(max_length=2, choices=SECTORS)
    web = models.CharField("Web", max_length=200, blank=True)
    PROJECT_STATUS_OPTIONS = (
        ("IN_MEDITATION_PROCESS", "En proces de debat/reflexió"),
        ("IN_CONSTITUTION_PROCESS", "En constitució"),
        ("RUNNING", "Constituïda"),
        ("DOWN", "Caigut")
    )
    project_status = models.CharField("estat del projecte", max_length=50,
                                      blank=True, null=True,
                                      choices=PROJECT_STATUS_OPTIONS)
    MOTIVATION_OPTIONS = (
        ('COOPERATIVISM_EDUCATION', 'Formació en cooperativisme'),
        ('COOPERATIVE_CREATION', "Constitució d'una cooperativa"),
        ('TRANSFORM_FROM_ASSOCIATION',
         "Transformació d'associació a cooperativa"),
        ('TRANSFORM_FROM_SCP', "Transformació de SCP a cooperativa"),
        ('ENTERPRISE_RELIEF', "Relleu empresarial"),
        ('CONSOLIDATION', "Consolidació"),
        ('OTHER', "Altres"),
    )
    motivation = models.CharField("petició inicial", max_length=50, blank=True,
                                  null=True, choices=MOTIVATION_OPTIONS)
    mail = models.EmailField("correu electrònic")
    phone = models.CharField("telèfon", max_length=25)
    town = models.ForeignKey(Town, verbose_name="població",
                             on_delete=models.SET_NULL, null=True, blank=True)
    district = models.TextField("districte", blank=True, null=True,
                                choices=settings.DISTRICTS)
    number_people = models.IntegerField("número de persones", blank=True,
                                        null=True)
    registration_date = models.DateField("data de registre", blank=True,
                                         null=True,
                                         default=datetime.date.today)
    cif = models.CharField("N.I.F.", max_length=11, blank=True, null=True)
    object_finality = models.TextField("objecte i finalitat", blank=True,
                                       null=True)
    project_origins = models.TextField("orígens del projecte", blank=True,
                                       null=True)
    solves_necessities = models.TextField(
        "quines necessitats resol el vostre projecte?", blank=True, null=True)
    social_base = models.TextField(
        "compta el vostre projecte amb una base social?", blank=True,
        null=True)
    constitution_date = models.DateField("data de constitució", blank=True,
                                         null=True)
    subsidy_period = models.ForeignKey(
        SubsidyPeriod, verbose_name="convocatòria de la constitució",
        null=True, blank=True, on_delete=models.SET_NULL,
        help_text="OPCIONAL. En cas que el projecte s'hagi constituït en una "
                  "convocatòria posterior a l'ultima "
                  "intervenció de l'ateneu, podeu indicar-ho aquí, per tal "
                  "que aparegui a l'informe de Projectes "
                  "Constituïts. Aquest camp NO farà aparèixer el projecte a "
                  "l'excel de justificació (per aparèixer a "
                  "l'excel cal crear una Justificació d'Acompanyament)"
    )
    estatuts = models.FileField("estatuts", blank=True, null=True,
                                storage=PrivateMediaStorage(), max_length=250)
    viability = models.FileField("pla de viabilitat", blank=True, null=True,
                                 storage=PrivateMediaStorage(),
                                 max_length=250)
    sostenibility = models.FileField("pla de sostenibilitat", blank=True,
                                     null=True, storage=PrivateMediaStorage(),
                                     max_length=250)
    derivation = models.ForeignKey(Derivation, verbose_name="derivat",
                                   on_delete=models.SET_NULL, blank=True,
                                   null=True)
    derivation_date = models.DateField("data de derivació", blank=True,
                                       null=True)
    description = models.TextField("descripció", blank=True, null=True)
    other = models.CharField(
        "altres", max_length=240, blank=True, null=True,
        help_text="Apareix a la taula de Seguiment d'Acompanyaments")
    employment_estimation = models.PositiveIntegerField(
        "insercions laborals previstes", default=0)
    follow_up_situation = models.CharField("seguiment", max_length=50,
                                           choices=settings.PROJECT_STATUS,
                                           blank=True,
                                           null=True)
    follow_up_situation_update = models.DateTimeField(
        "actualització seguiment", blank=True, null=True)
    tags = tagulous.models.TagField(
        verbose_name="etiquetes",
        force_lowercase=True, blank=True,
        help_text="Prioritza les etiquetes que apareixen auto-completades. Si "
                  "escrius una etiqueta amb un espai creurà que son dues "
                  "etiquetes, per evitar-ho escriu-la entre cometes dobles, "
                  "\"etiqueta amb espais\"."
    )

    @property
    def has_estatus(self):
        if self.estatuts:
            return True
        else:
            return False

    @property
    def has_viability(self):
        if self.viability:
            return True
        else:
            return False

    @property
    def has_sostenibility(self):
        if self.sostenibility:
            return True
        else:
            return False

    @property
    def stages_list(self):
        if not self.stages or self.stages.count() < 1:
            return None
        stages = []
        for stage in self.stages.all():
            name = stage.get_stage_type_display()
            if stage.stage_subtype:
                name = f"{name} ({stage.stage_subtype.name})"
            stages.append(name)
        stages.sort()
        return "; ".join(stages)

    @property
    def axis_list(self):
        """
        This method is not used in the new data, reports or exports
        since 1/11/2021, but needs to be kept until it's confirmed that they
        don't want the old exports.
        :return:
        """
        if not self.stages or self.stages.count() < 1:
            return None
        stages = []
        for stage in self.stages.all():
            stages.append(stage.axis_summary())
        stages.sort()
        return "; ".join(stages)

    @property
    def services_list(self):
        if not self.stages or self.stages.count() < 1:
            return None
        stages = [stage.get_service_display() for stage in self.stages.all() if stage.service]
        return "; ".join(stages)

    @property
    def last_stage_responsible(self):
        if not self.stages or self.stages.count() < 1:
            return None
        return self.stages.all()[0].stage_responsible

    last_stage_responsible.fget.short_description = "Últim acompanyament"

    @property
    def last_stage_organizer(self):
        if not self.stages or self.stages.count() < 1:
            return None
        return self.stages.all()[0].stage_organizer

    last_stage_organizer.fget.short_description = "Última organitzadora"

    @property
    def full_town_district(self):
        if not self.town:
            return None
        ret = self.town
        if self.district:
            ret = f"{ret} ({self.get_district_display()})"
        return ret

    @property
    def follow_up_with_date(self):
        if self.follow_up_situation_update:
            date = self.follow_up_situation_update.strftime('%d-%m-%Y')
            return f"{self.follow_up_situation} ({date})"
        return self.follow_up_situation

    @staticmethod
    def autocomplete_search_fields():
        return ('name__icontains',)

    @property
    def partners_activities(self):
        acts = []
        for partner in self.partners.all():
            for activity in partner.enrolled_activities.all():
                if activity not in acts:
                    activity = f"{activity.date_start}: {activity}"
                    acts.append(activity)
        acts.sort()
        return mark_safe("<br>".join(acts))

    partners_activities.fget.short_description = "Sessions"

    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Project.objects.get(pk=self.pk)
            if orig.follow_up_situation != self.follow_up_situation:
                self.follow_up_situation_update = now()
        super(Project, self).save(*args, **kw)

    def __str__(self):
        return self.name


class StageSubtype(models.Model):
    class Meta:
        verbose_name = "subtipus"
        verbose_name_plural = "subtipus"

    name = models.CharField("nom", max_length=200, blank=False, unique=True,
                            null=False)

    def __str__(self):
        return self.name


class ProjectFile(models.Model):
    class Meta:
        verbose_name = "fitxer"
        verbose_name_plural = "fitxers"
        ordering = ["name"]

    image = models.FileField(
        "fitxer",
        storage=PublicMediaStorage(),
        max_length=250
    )
    name = models.CharField(
        "Etiqueta",
        max_length=250,
        null=False,
        blank=False,
        help_text="Els fitxers antics tenen com a etiqueta el propi nom de "
                  "l'arxiu, però aquí hi pot anar qualsevol text descriptiu."
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="files"
    )

    def __str__(self):
        return self.name


class ProjectStage(models.Model):
    class Meta:
        verbose_name = "justificació d'acompanyament"
        verbose_name_plural = "justificacions d'acompanyaments"
        ordering = ["-date_start"]

    DEFAULT_STAGE_TYPE = 1

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="projecte acompanyat",
        related_name="stages")
    STAGE_TYPE_OPTIONS = (
        ('11', "Creació"),
        ('12', "Consolidació"),
        ('9', "Incubació"),
    )
    stage_type = models.CharField("tipus d'acompanyament", max_length=2,
                                  default=DEFAULT_STAGE_TYPE,
                                  choices=STAGE_TYPE_OPTIONS)
    stage_subtype = models.ForeignKey(
        StageSubtype, verbose_name="subtipus", default=None, null=True,
        blank=True, on_delete=models.SET_NULL
    )
    subsidy_period = models.ForeignKey(
        SubsidyPeriod, verbose_name="convocatòria", null=True,
        on_delete=models.SET_NULL)
    date_start = models.DateField(
        "data creació acompanyament", null=False, blank=False,
        auto_now_add=True
    )
    service = models.SmallIntegerField(
        "Servei",
        choices=ServicesChoices.choices,
        null=True,
        blank=True,
    )
    axis = models.CharField(
        "(OBSOLET) Eix", help_text="Eix de la convocatòria on es justificarà.",
        choices=settings.AXIS_OPTIONS, null=True, blank=True, max_length=1)
    subaxis = models.CharField(
        "(OBSOLET) Sub-eix", help_text="Correspon a 'Tipus d'acció' a la justificació.",
        null=True, blank=True, max_length=2, choices=get_subaxis_choices())
    circle = models.SmallIntegerField(
        "Ateneu / Cercle",
        choices=CirclesChoices.choices_named(),
        null=True,
        blank=True,
    )
    # Entity was called "organizer" before, causing confusion, specially
    # because we wanted to add the Organizer field
    # here. We renamed 'organizer' to entity and made a migration for this
    # change (0046_auto...py).
    # Then I added the 'organizer' FK field. Makemigration worked fine, but
    # migrate was throwing an error:
    #   django.db.utils.ProgrammingError: relation
    #   "coopolis_projectstage_organizer_id_26459182" already exists
    # In the database everything was correct, not a field or a key in
    # coopolis_projectstage table called 'organizer'
    # or any other reference, also not postgres cache glitches or anything I
    # could identify.
    # Did the experiment of calling it differently and worked.
    # Given that I don't understand the problem, leaving the field with a
    # different name seems the safest option.
    stage_organizer = models.ForeignKey(
        Organizer, verbose_name="organitzadora", on_delete=models.SET_NULL,
        null=True, blank=True)
    stage_responsible = models.ForeignKey(
        "User", verbose_name="persona responsable", blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='stage_responsible',
        help_text="Persona de l'equip al càrrec de l'acompanyament. Per "
                  "aparèixer al desplegable, cal que la persona tingui "
                  "activada la opció 'Membre del personal'.")
    scanned_certificate = models.FileField(
        "Certificat", blank=True, null=True,
        storage=PrivateMediaStorage(), max_length=250)
    involved_partners = models.ManyToManyField(
        User, verbose_name="persones involucrades", blank=True,
        related_name='stage_involved_partners',
        help_text="Persones que apareixeran a la justificació com a que han "
                  "participat a l'acompanyament.")

    # cofunding options module
    cofunded = models.ForeignKey(
        Cofunding, verbose_name="Cofinançat", on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cofunded_projects')
    cofunded_ateneu = models.BooleanField(
        "Cofinançat amb Ateneus Cooperatius", default=False)
    strategic_line = models.ForeignKey(
        StrategicLine, verbose_name="línia estratègica",
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name='strategic_line_projects')

    def axis_summary(self):
        axis = self.axis if self.axis else '(cap)'
        subaxis = self.subaxis if self.subaxis else '(cap)'
        return f"{axis}-{subaxis}"

    axis_summary.short_description = "Eix - Subeix"
    axis_summary.admin_order_field = 'axis'

    def hours_sum(self):
        total_qs = self.stage_sessions.aggregate(
            total_sum=Sum('hours')
        )
        total = 0 if not total_qs['total_sum'] else total_qs['total_sum']
        return total
    hours_sum.short_description = "Suma d'hores"

    def sessions_count(self):
        return len(self.stage_sessions.all())
    sessions_count.short_description = "Nº sessions"

    def clean(self):
        super().clean()
        if self.axis:
            subaxis_options = get_subaxis_for_axis(str(self.axis))
            if self.subaxis not in subaxis_options:
                raise ValidationError(
                    {'subaxis': "Has seleccionat un sub-eix que no es "
                                "correspon a l'eix."}
                )

    def get_full_type_str(self):
        txt = self.get_stage_type_display()
        if config.ENABLE_STAGE_SUBTYPES and self.stage_subtype:
            txt = f"{txt} ({self.stage_subtype.name})"
        return txt

    @property
    def latest_session(self):
        try:
            return self.stage_sessions.latest("date")
        except ProjectStageSession.DoesNotExist:
            return None

    def __str__(self):
        txt = (f"{str(self.project)}: {self.get_full_type_str()} "
               f"[{str(self.subsidy_period)}]")
        return txt


class ProjectStageSession(models.Model):
    class Meta:
        verbose_name = "Sessió d'acompanyament"
        verbose_name_plural = "Sessions d'acompanyament"

    project_stage = models.ForeignKey(
        ProjectStage, on_delete=models.CASCADE, related_name="stage_sessions",
        verbose_name="justificació d'acompanyament"
    )
    session_responsible = models.ForeignKey(
        "User", verbose_name="persona facilitadora", blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='stage_sessions',
        help_text="Persona de l'equip que ha facilitat la sessió. Per "
                  "aparèixer al desplegable, cal que la persona tingui "
                  "activada la opció 'Membre del personal'.")
    date = models.DateField(
        "data",
        default=datetime.date.today,
        null=True, blank=False
    )
    hours = models.FloatField(
        "número d'hores",
        help_text="Camp necessari per la justificació.",
        null=True,
        blank=True,
    )
    follow_up = models.TextField("seguiment", null=True, blank=True)
    entity = models.ForeignKey(
        Entity, verbose_name="Entitat", default=None, null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return (f"Sessió d'acompanyament del {self.date} per "
                f"{self.project_stage.project.name}")


class ProjectsFollowUp(Project):
    """
    Deprecated: from Nov 2021 this is kept to let them access older reports,
    but when they don't need them anymore this and the corresponding admin view
    and template can be deleted.
    """
    class Meta:
        proxy = True
        verbose_name_plural = "(obsolet) Seguiment d'acompanyaments per eix"
        verbose_name = "(obsolet) Seguiment d'acompanyament per eix"
        ordering = ['follow_up_situation', 'follow_up_situation_update']


class ProjectsFollowUpService(Project):
    class Meta:
        proxy = True
        verbose_name_plural = "Seguiment d'acompanyaments"
        verbose_name = "Seguiment d'acompanyament"
        ordering = ['follow_up_situation', 'follow_up_situation_update']


class ProjectsConstituted(Project):
    """
    Deprecated: from Nov 2021 this is kept to let them access older reports,
    but when they don't need them anymore this and the corresponding admin view
    and template can be deleted.
    """
    class Meta:
        proxy = True
        verbose_name_plural = "(obsolet) Projectes constituïts per eix"
        verbose_name = "(obsolet) Projecte constituït per eix"


class ProjectsConstitutedService(Project):
    class Meta:
        proxy = True
        verbose_name_plural = "Projectes constituïts"
        verbose_name = "Projecte constituït"


class EmploymentInsertion(models.Model):
    class Meta:
        verbose_name = "inserció laboral"
        verbose_name_plural = "insercions laborals"
        ordering = ["-insertion_date"]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="projecte acompanyat",
        related_name="employment_insertions")
    user = models.ForeignKey(
        User, verbose_name="persona", blank=True, null=True,
        on_delete=models.PROTECT)
    subsidy_period = models.ForeignKey(
        SubsidyPeriod, verbose_name="convocatòria", null=True,
        on_delete=models.SET_NULL)
    insertion_date = models.DateField("alta seguretat social")
    end_date = models.DateField("baixa seg. social", null=True, blank=True)
    CONTRACT_TYPE_CHOICES = (
        (1, "Indefinit"),
        (5, "Temporal"),
        (2, "Formació i aprenentatge"),
        (3, "Pràctiques"),
        (4, "Soci/a cooperativa o societat laboral")
    )
    contract_type = models.SmallIntegerField(
        "tipus de contracte",
        choices=CONTRACT_TYPE_CHOICES,
        null=True
    )
    circle = models.SmallIntegerField(
        "Ateneu / Cercle",
        choices=CirclesChoices.choices_named(),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.full_name}: {self.get_contract_type_display()}"
