import datetime

from constance import config
from django.conf import settings
from django.db import models
from django.db.models import Sum, Q
from django.utils.safestring import mark_safe
from django.utils.timezone import now
import tagulous.models

from apps.cc_courses.models import Entity, Organizer, Activity
from apps.coopolis.choices import ServicesChoices, SubServicesChoices
from apps.cc_users.models import User
from apps.towns.models import Town
from apps.coopolis.storage_backends import PrivateMediaStorage, PublicMediaStorage
from apps.dataexports.models import SubsidyPeriod
from conf.custom_mail_manager import MyMailTemplate


class Derivation(models.Model):
    class Meta:
        verbose_name = "derivació"
        verbose_name_plural = "derivacions"
        ordering = ["name"]

    name = models.CharField("nom", max_length=250)

    def __str__(self):
        return self.name


class Project(models.Model):
    class Meta:
        verbose_name_plural = "projectes"
        verbose_name = "projecte"

    partners = models.ManyToManyField(
        User,
        verbose_name="sòcies o membres del projecte",
        blank=True,
        related_name="projects",
    )
    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    SECTORS = (
        ('M', 'Alimentació'),
        ('S', 'Assessorament'),
        ('A', 'Altres'),
        ('C', 'Comunicació i tecnologia'),
        ('CU', 'Cultura'),
        ('U', 'Cures'),
        ('E', 'Educació'),
        ('F', 'Finances'),
        ('H', 'Habitatge'),
        ('L', 'Logística'),
        ('O', 'Oci'),
        ('R', 'Roba')
    )
    sector = models.CharField(max_length=2, choices=SECTORS)
    web = models.CharField("xarxes socials", max_length=200, blank=True)
    PROJECT_STATUS_OPTIONS = (
        ("IN_MEDITATION_PROCESS", "En procés de debat/reflexió"),
        ("IN_CONSTITUTION_PROCESS", "En constitució"),
        ("RUNNING", "Constituïda"),
        ("IN_CONSOLIDATION_PROCESS", "En procés de consolidació"),
        ("DOWN", "Caigut")
    )
    project_status = models.CharField("estat del projecte", max_length=50,
                                      blank=True, null=True,
                                      choices=PROJECT_STATUS_OPTIONS)
    MOTIVATION_OPTIONS = (
        ('CONSOLIDATION', "Consolidació"),
        ('TERRITORIAL_ARRANGEMENT', 'Arrelament territorial'),
        ('OTHER', "Altres"),
    )
    motivation = models.CharField("petició inicial", max_length=50, blank=True,
                                  null=True, choices=MOTIVATION_OPTIONS)
    mail = models.EmailField("correu electrònic")
    phone = models.CharField("telèfon", max_length=25)
    town = models.ForeignKey(Town, verbose_name="població",
                             on_delete=models.SET_NULL, null=True, blank=True)
    neighborhood = models.CharField(
        "Barri",
        default="",
        blank=True,
        max_length=50,
    )
    number_people = models.IntegerField("número de persones", blank=True,
                                        null=True)
    registration_date = models.DateField("data de registre", blank=True,
                                         null=True,
                                         default=datetime.date.today)
    cif = models.CharField("N.I.F.", max_length=11, blank=True, null=True)
    object_finality = models.TextField("objecte i finalitat", blank=True,
                                       null=True)
    project_origins = models.TextField("descripció del projecte", blank=True,
                                       null=True)
    solves_necessities = models.TextField(
        "quines necessitats resol el vostre projecte?", blank=True, null=True)
    social_base = models.TextField(
        "base social (quines entitats o persones en formen part)", blank=True,
        null=True)
    constitution_date = models.DateField("data de constitució", blank=True,
                                         null=True)
    subsidy_period = models.ForeignKey(
        SubsidyPeriod, verbose_name="convocatòria de la constitució",
        null=True, blank=True, on_delete=models.SET_NULL,
        help_text="OPCIONAL. En cas que el projecte s'hagi constituït en una "
                  "convocatòria posterior a l'ultima "
                  "intervenció de la comunalitat, podeu indicar-ho aquí, per tal "
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
    def services_list(self):
        if not self.stages or self.stages.count() < 1:
            return None
        stages = [stage.get_service_display() for stage in self.stages.all() if stage.service]
        return "; ".join(stages)

    @property
    def last_stage_responsible(self):
        if not self.stages or self.stages.count() < 1:
            return None
        return self.stages.all()[0].responsible

    last_stage_responsible.fget.short_description = "Últim acompanyament"

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

    partners_activities.fget.short_description = "Activitats"

    @property
    def partners_participants(self):
        """
        To display the list of all the people who participated in project
        stage sessions.
        """
        if not self.id:
            return "-"
        participants = User.objects.filter(
            stage_sessions_participated__project_stage__project=self,
        ).distinct()
        participants_strings = [str(x) for x in participants]
        participants_strings.sort()
        return mark_safe(", ".join(participants_strings))

    partners_participants.fget.short_description = (
        "Participants a sessions d'acompanyament"
    )

    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Project.objects.get(pk=self.pk)
            if orig.follow_up_situation != self.follow_up_situation:
                self.follow_up_situation_update = now()
        super(Project, self).save(*args, **kw)

    def notify_new_request_to_comunalitat(self):
        if not config.CONTACT_EMAIL:
            return
        mail = MyMailTemplate('EMAIL_NEW_PROJECT')
        mail.to = config.CONTACT_EMAIL.split(',')
        mail.subject_strings = {
            'projecte_nom': self.name
        }
        mail.body_strings = {
            'projecte_nom': self.name,
            'projecte_telefon': self.phone,
            'projecte_email': self.mail,
            'usuari_email': self.partners.all()[0].email,
        }
        mail.send()

    def notify_request_confirmation(self):
        mail = MyMailTemplate('EMAIL_PROJECT_REQUEST_CONFIRMATION')
        mail.subject_strings = {
            'projecte_nom': self.name
        }
        mail.body_strings = {
            'projecte_nom': self.name,
            'url_backoffice': settings.ABSOLUTE_URL,
        }
        mail.send_to_user(self.partners.all()[0])

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
        ('13', "Creixement"),
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
    sub_service = models.SmallIntegerField(
        "Sub-servei",
        choices=SubServicesChoices.choices,
        null=True,
        blank=True,
    )
    organizer = models.ForeignKey(
        Organizer, verbose_name="organitzadora", on_delete=models.SET_NULL,
        null=True, blank=True)
    responsible = models.ForeignKey(
        User,
        verbose_name="persona responsable",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='stage_responsible',
        help_text="Persona de l'equip al càrrec de l'acompanyament. Per "
        "aparèixer al desplegable, cal que la persona tingui "
        "activada la opció 'Membre del personal'.",
    )
    scanned_certificate = models.FileField(
        "Document justificació final", blank=True, null=True,
        storage=PrivateMediaStorage(), max_length=250)
    involved_partners = models.ManyToManyField(
        User, verbose_name="(obsolet) Persones involucrades", blank=True,
        related_name='stage_involved_partners',
        help_text="Persones que apareixeran a la justificació com a que han "
                  "participat a l'acompanyament.")

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

    def get_full_type_str(self):
        txt = self.get_stage_type_display()
        if self.stage_subtype:
            txt = f"{txt} ({self.stage_subtype.name})"
        return txt

    @property
    def latest_session(self):
        try:
            return self.stage_sessions.latest("date")
        except ProjectStageSession.DoesNotExist:
            return None

    @property
    def involved_partners_count(self):
        return self.partners_involved_in_sessions.count()

    @property
    def partners_involved_in_sessions(self):
        return User.objects.filter(
            stage_sessions_participated__in=self.stage_sessions.all()
        ).distinct()

    @property
    def justification_documents_total(self):
        docs_count = self.stage_sessions.exclude(
            Q(justification_file='') | Q(justification_file=None),
        ).count()
        return f"{docs_count} / {self.stage_sessions.count()}"
    justification_documents_total.fget.short_description = "Docs justif."

    @property
    def entities_str(self):
        sessions = self.stage_sessions.filter(entity__isnull=False).distinct("entity")
        entities_list = [str(x.entity) for x in sessions]
        entities_list.sort()
        return ", ".join(entities_list)

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
        User,
        verbose_name="persona facilitadora",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='stage_sessions',
        help_text="Persona de l'equip que ha facilitat la sessió. Per "
        "aparèixer al desplegable, cal que la persona tingui "
        "activada la opció 'Membre del personal'.",
    )
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
    # Aquest camp Entity no apareix enlloc, pendent que confirmin si és correcte que no hi ha de ser
    # per marcar-lo com a obsolet o bé ja eliminar-lo.
    entity = models.ForeignKey(
        Entity, verbose_name="Entitat", default=None, null=True, blank=True,
        on_delete=models.SET_NULL)
    involved_partners = models.ManyToManyField(
        User, verbose_name="persones involucrades", blank=True,
        related_name='stage_sessions_participated',
        help_text="Persones que apareixeran a la justificació com a que han "
                  "participat a la sessió d'acompanyament.")
    justification_file = models.FileField(
        "fitxer de justificació",
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
    )

    @property
    def project_partners(self):
        partners = self.project_stage.project.partners.all()
        partners_list = [str(x) for x in partners]
        partners_list.sort()
        return ", ".join(partners_list)

    project_partners.fget.short_description = "Persones sòcies"

    def __str__(self):
        return (f"Sessió d'acompanyament del {self.date} per "
                f"{self.project_stage.project.name}")


class ProjectsFollowUpService(Project):
    class Meta:
        proxy = True
        verbose_name_plural = "Seguiment d'acompanyaments"
        verbose_name = "Seguiment d'acompanyament"
        ordering = ['follow_up_situation', 'follow_up_situation_update']


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

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        verbose_name="activitat relacionada amb l'inserció",
        related_name="employment_insertions",
    )
    user = models.ForeignKey(
        User,
        verbose_name="persona",
        on_delete=models.PROTECT,
    )
    subsidy_period = models.ForeignKey(
        SubsidyPeriod, verbose_name="convocatòria", null=True,
        on_delete=models.SET_NULL)
    insertion_date = models.DateField("alta seguretat social")
    end_date = models.DateField("baixa seg. social", null=True, blank=True)
    CONTRACT_TYPE_CHOICES = (
        (1, "Indefinit"),
        (5, "Temporal"),
        (2, "Soci/a cooperativa o societat laboral"),
        (3, "Autònom"),
    )
    contract_type = models.SmallIntegerField(
        "tipus de contracte",
        choices=CONTRACT_TYPE_CHOICES,
        null=True
    )
    entity_name = models.CharField(
        "Nom de l'entitat on s'insereix",
        max_length=150,
    )
    entity_nif = models.CharField(
        "NIF de l'entitat on s'insereix",
        max_length=11,
    )
    entity_town = models.ForeignKey(
        "towns.Town",
        verbose_name="població de l'entitat on s'insereix",
        on_delete=models.SET_NULL,
        null=True,
    )
    entity_neighborhood = models.CharField(
        "Barri de l'entitat on s'insereix",
        max_length=50,
    )

    def __str__(self):
        return f"{self.user.full_name}: {self.get_contract_type_display()}"
