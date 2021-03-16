from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.urls import reverse

from coopolis.models import ProjectStage
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

    def handle(self, *args, **options):
        data_consolidation_pending, report = self.make_report()
        if data_consolidation_pending:
            self.stdout.write(report)
        else:
            if options['migrate']:
                self.migrate()

            report = """
            <h2>Totes les justificacions d'acompanyament tenen les dades 
            consolidades i podran ser migrades. Gràcies!</h2>
            <p><strong>Propers passos:</strong></p>
            <ul>
              <li>És molt important que en les properes setmanes us assegureu 
              que tothom de l'equip que toqui justificacions d'acompanyament 
              mantingui les dades consolidades, per tal que quan arribi el dia
              que executem la migració, funcioni correctament.</li>
              <li>Si us plau avisa al Pere (pere@codi.coop) de que heu acabat 
              aquest procés.</li>
              <li>Quan la resta d'ateneus implicats hagin acabat el procés
              podrem continuar amb la migració.</li>
              <li>Abans de fer la migració amb les dades reals, farem una
              simulació al servidor de proves que haurem de verificar. Ja us
              contactaré quan estigui a punt.</li>
            </ul>
            """
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
            self.stdout.write(f"<h1>Convocatòria {period}</h1>")
            projects = self.get_projects(period)
            self.stdout.write(f'<p>Total projects: {len(projects)}</p>')
            for project, values in projects.items():
                stage_types = values['stage_types']
                project_obj = values['obj']
                url = self.get_obj_url(project_obj)
                stage_types_report = list()
                for stage_type, stages in stage_types.items():
                    stage_type_report = f"<h3>Processant el tipus {stage_type}</h3>"
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
                      <td>Entitat</td>
                      <td>Organitzadora</td>
                      <td>Fitxa projectes</td>
                      <td>Certificat</td>
                    </tr>
                    """

                    for stage in stages:
                        date = f"<strong>{stage.date_start.strftime('%d.%m.%Y')}</strong>"
                        url = self.get_obj_url(stage, date)
                        stage_type_report += f"""
                        <tr>
                          <td>{url}</td>
                          <td>{project}</td>
                          <td>{stage.get_stage_type_display()}</td>
                          <td>{stage.axis_summary()}</td>
                          <td>{stage.entity}</td>
                          <td>{stage.stage_organizer}</td>
                          <td>{stage.scanned_signatures}</td>
                          <td>{stage.scanned_certificate}</td>
                        </tr>
                        """
                    stage_type_report += '</table>'

                    if self.has_data_coherence(stages) is False:
                        stage_types_report.append(stage_type_report)
                if len(stage_types_report) > 0:
                    project_report = f'<h2>Processant el projecte {url}</h2>'
                    report += project_report
                    report += "".join(stage_types_report)
                    data_consolidation_pending = True

        return data_consolidation_pending, report

    @staticmethod
    def has_data_coherence(stages):
        axises = set()
        subaxises = set()
        entities = set()
        organizers = set()
        signatures = set()
        certificates = set()
        for stage in stages:
            if stage.axis:
                axises.add(stage.axis)
            if stage.subaxis:
                subaxises.add(stage.subaxis)
            if stage.entity:
                entities.add(stage.entity)
            if stage.stage_organizer:
                organizers.add(stage.stage_organizer)
            if stage.scanned_signatures:
                signatures.add(stage.scanned_signatures)
            if stage.scanned_certificate:
                certificates.add(stage.scanned_certificate)
        if (
            len(axises) > 1
            or len(subaxises) > 1
            or len(entities) > 1
            or len(organizers) > 1
            or len(signatures) > 1
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
            if pname not in projects:
                projects[pname] = {
                    'obj': stage.project,
                    'stage_types': {
                        stype: [stage, ],
                    },
                }
            else:
                if stype not in projects[pname]['stage_types']:
                    projects[pname]['stage_types'][stype] = [stage, ]
                else:
                    projects[pname]['stage_types'][stype].append(
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

    def migrate(self):
        # MERGING: Aquesta versió no conté la migració real ja que està pensada
        # per una branch com la que hi ha a producció, sense els canvis de
        # l'últim sprint.
        # La versió que conté la migració real és a la branch
        # projectstage_sessions, que està basada en la branch sprint_2021_03.
        periods = self.get_subsidy_periods()
        for period in periods:
            self.stdout.write(f"<h1>Migrant convocatòria {period}</h1>")
            projects = self.get_projects(period)
            self.stdout.write(f'<p>Total projects: {len(projects)}</p>')
            for project, values in projects.items():
                stage_types = values['stage_types']
                for stage_type, stages in stage_types.items():
                    self.stdout.write(f"<h3>Processant el tipus {stage_type}</h3>")
                    for stage in stages:
                        self.stdout.write(f"""TO DO amb {stage}:
                        - Crear StageSession amb les hores, text, etc. dins 
                         l'stage principal.
                        - Afegir els Participants d'aquest stage a l'stage 
                        principal (els que no hi siguin ja). 
                        - Eliminar aquest stage (si no és el principal).
                        """)
