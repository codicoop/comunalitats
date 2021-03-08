from django.core.management.base import BaseCommand
from django.db.models import Count

from coopolis.models import ProjectStage, Project
from dataexports.models import SubsidyPeriod


class Command(BaseCommand):
    help = ("Goes through all ProjectStage's to migrate them into the new "
            "structure of ProjectStageSession's.")

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Generates the report without modifying the database.',
        )

    def handle(self, *args, **options):
        if options['dry_run']:
            print('running dry!')

        periods = self.get_subsidy_periods()
        for period in periods:
            print(f"<h1>Convocatòria {period}</h1>")
            projects = self.get_projects(period)
            print(f'<p>Total projects: {projects}</p>')
            for project, stage_types in projects.items():
                print(f'<h2>Processant el projecte {project}</h2>')
                # TODO: fer servir settings.ABSOLUTE_URL per generar la
                # del projecte a l'informe.
                for stage_type, stages in stage_types.items():
                    print(f"<h3>Processant el tipus {stage_type}</h3>")
                    print("Sessió d'acompanyament principal: ", stages[0])
                    print('Total de sessions: ', len(stages))
                    for stage in stages:
                        print('Processant stage: ', stage)

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
            if stage.project.name not in projects:
                projects[stage.project.name] = {
                    stage.get_stage_type_display: [stage, ],
                }
            else:
                if stage.get_stage_type_display not in projects[stage.project.name]:
                    projects[stage.project.name][stage.get_stage_type_display] = [stage, ]
                else:
                    projects[stage.project.name][stage.get_stage_type_display].append(
                        stage
                    )
        return projects
