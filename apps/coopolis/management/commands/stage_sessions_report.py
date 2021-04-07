from constance import config
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.urls import reverse

from coopolis.models import ProjectStage
from coopolis.models.projects import ProjectStageSession, ProjectFile
from dataexports.models import SubsidyPeriod


class Command(BaseCommand):
    help = ("Goes through all ProjectStage's to migrate them into the new "
            "structure of ProjectStageSession's.")

    def add_arguments(self, parser):
        parser.add_argument(
            '--migrate',
            action='store_true',
            help='Checks if the data is suitable for migrating and performs '
                 'the migration.',
        )
        parser.add_argument(
            '--check',
            action='store_true',
            help='Checks if the data is suitable for migrating.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Disables any change in the database.',
        )

    def handle(self, *args, **options):
        data_consolidation_pending, report = self.make_report()
        if options['check']:
            if data_consolidation_pending:
                m = f"{settings.PROJECT_NAME}: té dades pendents per revisar."
            else:
                m = f"{settings.PROJECT_NAME}: dades OK, pot migrar."
            self.stdout.write(m)
            return

        if options['migrate']:
            if data_consolidation_pending:
                m = (f"No és possible fer la migració, {settings.PROJECT_NAME}"
                     f" té dades pendents per revisar.")
                self.stdout.write(m)
                return
            report = self.migrate(options['dry_run'])

        self.stdout.write(report)

    def make_report(self):
        data_consolidation_pending = False
        report = """
        <style>
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
            }
            td {
               padding: 0 10px 0 10px;
            }
        </style>
        """
        periods = self.get_subsidy_periods()
        for period in periods:
            report += f"<h1>Convocatòria {period}</h1>"
            projects = self.get_projects(period)
            report += f'<p>Total projects: {len(projects)}</p>'
            for project, values in projects.items():
                stage_types = values['stage_types']
                project_obj = values['obj']
                url = self.get_obj_url(project_obj)
                stage_types_report = list()
                for stage_type, stage_subtypes in stage_types.items():
                    stage_type_report = f"<h3>Processant el tipus: {stage_type}</h3>"
                    for stage_subtype, stages in stage_subtypes['stage_subtypes'].items():
                        stage_type_report += f"<h4>Processant el subtipus: {stage_subtype}</h4>"

                        date = '-'
                        if stages[0].date_start:
                            date = f"<strong>{stages[0].date_start.strftime('%d.%m.%Y')}</strong>"
                        url = self.get_obj_url(stages[0])
                        stage_type_report += f"""
                        <p>Sessió d'acompanyament principal: {date} {url}</p>
                        <p>Total de sessions: {len(stages)}</p>
                        <table>
                        <tr>
                          <td>Data</td>
                          <td>Projecte</td>
                          <td>Tipus</td>
                          <td>Eix</td>
                          <td>Organitzadora</td>
                          <td>Certificat</td>
                          <td>Participants</td>
                        </tr>
                        """

                        for stage in stages:
                            date = '-'
                            if stage.date_start:
                                date = f"<strong>{stage.date_start.strftime('%d.%m.%Y')}</strong>"
                            url = self.get_obj_url(stage, date)
                            stage_type_report += f"""
                            <tr>
                              <td>{url}</td>
                              <td>{project}</td>
                              <td>{stage.get_stage_type_display()}</td>
                              <td>{stage.axis_summary()}</td>
                              <td>{stage.stage_organizer}</td>
                              <td>{stage.scanned_certificate}</td>
                              <td>{self.get_involved_partners_str(stage)}</td>
                            </tr>
                            """
                        stage_type_report += '</table>'

                        if self.has_data_coherence(stages) is False:
                            stage_types_report.append(stage_type_report)
                if len(stage_types_report) > 0:
                    project_report = f'<h2>Processant el projecte: {project_obj.name} {url}</h2>'
                    report += project_report
                    report += "".join(stage_types_report)
                    data_consolidation_pending = True

        return data_consolidation_pending, report

    @staticmethod
    def has_data_coherence(stages):
        axises = set()
        subaxises = set()
        organizers = set()
        certificates = set()
        for stage in stages:
            if stage.axis:
                axises.add(stage.axis)
            if stage.subaxis:
                subaxises.add(stage.subaxis)
            if stage.stage_organizer:
                organizers.add(stage.stage_organizer)
            if stage.scanned_certificate:
                certificates.add(stage.scanned_certificate)
        if (
            len(axises) > 1
            or len(subaxises) > 1
            or len(organizers) > 1
            or len(certificates) > 1
        ):
            return False
        else:
            return True

    @staticmethod
    def get_subsidy_periods():
        obj = SubsidyPeriod.objects.order_by('date_start').all()
        return obj

    @staticmethod
    def get_projects(period):
        stages = (
            ProjectStage
            .objects
            .filter(subsidy_period=period)
            .order_by('date_start')
            .all()
        )
        projects = dict()
        for stage in stages:
            pname = stage.project.name
            stype = stage.get_stage_type_display()
            ssubtype = None
            if stage.stage_subtype:
                ssubtype = stage.stage_subtype.name
            if not config.ENABLE_STAGE_SUBTYPES:
                ssubtype = 'cap'
            if pname not in projects:
                projects[pname] = {
                    'obj': stage.project,
                    'stage_types': {
                        stype: {
                            'stage_subtypes': {
                                ssubtype: [stage, ],
                            },
                        },
                    },
                }
            else:
                if stype not in projects[pname]['stage_types']:
                    projects[pname]['stage_types'][stype] = {
                        'stage_subtypes': {
                            ssubtype: [stage, ],
                        },
                    }
                else:
                    if ssubtype not in projects[pname]['stage_types'][stype]['stage_subtypes']:
                        projects[pname]['stage_types'][stype]['stage_subtypes'][ssubtype] = [stage, ]
                    else:
                        projects[pname]['stage_types'][stype]['stage_subtypes'][ssubtype].append(
                            stage
                        )
        return projects

    def get_obj_url(self, model_obj, label=None):
        url = self.get_admin_url(model_obj)
        url = f"{settings.ABSOLUTE_URL}{url}"
        if not label:
            label = model_obj
        url = f'<a href="{url}" target="_blank">{label}</a>'
        return url

    @staticmethod
    def get_admin_url(model_obj):
        content_type = ContentType.objects.get_for_model(model_obj.__class__)
        return reverse(
            f"admin:{content_type.app_label}_{content_type.model}_change",
            args=(model_obj.id, )
        )

    @staticmethod
    def get_involved_partners_str(project_stage_obj):
        """Not used, can be deleted"""
        names = list()
        if len(project_stage_obj.involved_partners.all()) > 0:
            for partner in project_stage_obj.involved_partners.all():
                names.append(partner.get_full_name())
        return ", ".join(names)

    def migrate(self, dry_run):
        # MERGING: Aquesta versió que sí que fa la migració real i que, per
        # tant, necessita l'última versió de la app per funcionar.
        periods = self.get_subsidy_periods()
        report = ""
        for period in periods:
            report += f"<h1>Migrant convocatòria {period}</h1>"
            projects = self.get_projects(period)
            report += f'<p>Total projects: {len(projects)}</p>'
            for project, values in projects.items():
                project_obj = values['obj']
                stage_types = values['stage_types']
                for stage_type, stage_subtypes in stage_types.items():
                    report += f"<h3>Processant el tipus: {stage_type}</h3>"
                    for stage_subtype, stages in stage_subtypes['stage_subtypes'].items():
                        report += f"<h4>Processant el subtipus: {stage_subtype}</h4>"

                        main_stage = stages[0]

                        if len(main_stage.stage_sessions.all()):
                            if len(stages) < 2:
                                report += (
                                    "<p>JA CONTÉ StageSessions, i té"
                                    f"{len(stages)} Stages. Skipping."
                                )
                            else:
                                report += (
                                    '<h1 style="color: red">JA CONTÉ StageSessions,'
                                    f' i té {len(stages)} Stages. Skipping, però '
                                    f's\'ha de processar a ma!.'
                                )
                            continue

                        date = '-'
                        if main_stage.date_start:
                            date = f"<strong>{main_stage.date_start.strftime('%d.%m.%Y')}</strong>"
                        url = self.get_obj_url(stages[0])
                        report += f"<p>Sessió d'acompanyament principal: {date} {url}</p>"

                        ### DADES QUE S'HAN D'ACTUALITZAR A LA MAIN_STAGE
                        # Obtenir list de tots els participants.
                        participants = self.get_all_participants(stages)
                        participants_name = []
                        for participant in participants:
                            participants_name.append(participant.get_full_name())
                        participants_str = ", ".join(participants_name)
                        report += f"<p>Participants totals: {participants_str}</p>"
                        main_participants = len(main_stage.involved_partners.all())
                        total_participants = len(participants)
                        if main_participants != total_participants:
                            report += f"""
                            <p><strong>S'ha fet MERGE de participants.</strong></p>
                            <p>Participants main: {self.get_involved_partners_str(
                                main_stage
                            )}</p>
                            """
                            if not dry_run:
                                main_stage.involved_partners.set(participants)

                        for stage in stages:
                            new_session = ProjectStageSession()
                            new_session.project_stage = main_stage
                            new_session.hours = stage.hours
                            new_session.follow_up = stage.follow_up
                            new_session.date = stage.date_start
                            new_session.entity = stage.entity
                            new_session.session_responsible = stage.stage_responsible
                            if not dry_run:
                                new_session.save()

                            if stage.scanned_certificate:
                                main_stage.scanned_certificate = stage.scanned_certificate
                            if stage.scanned_signatures:
                                if not dry_run:
                                    ProjectFile.objects.create(
                                        image=stage.scanned_signatures,
                                        name=stage.scanned_signatures.name,
                                        project=project_obj
                                    )

                            if stage is not main_stage:
                                if not dry_run:
                                    stage.delete()

                        if not config.ENABLE_STAGE_SUBTYPES:
                            main_stage.stage_subtype = None

                        # main_stage ara conté els últims fitxers que s'hagin
                        # trobat a algun dels stages.
                        if not dry_run:
                            main_stage.save()
        return report

    @staticmethod
    def get_all_participants(stages):
        participants = set()
        for stage in stages:
            if len(stage.involved_partners.all()) > 0:
                participants.update(stage.involved_partners.all())
        return participants
