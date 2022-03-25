# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from datetime import date

from django.db import IntegrityError
from django_q.tasks import schedule

from apps.dataexports.models import SubsidyPeriod, DataExports


class Command(BaseCommand):
    help = 'Normalizes the minimum common data that every instance should have: ' \
           'user groups and convocatòries.'

    def handle(self, *args, **options):
        self.add_group_permissions()
        self.normalize_subsidy_periods()
        self.normalize_exports()
        self.create_schedules()

    @staticmethod
    def normalize_subsidy_periods():
        periods = (
            {
                'name': 'Sense justificar',
                'date_start': date(1975, 1, 1),
                'date_end': date(1975, 1, 1)
            },
            {
                'name': '2016-2017',
                'date_start': date(2016, 11, 1),
                'date_end': date(2017, 10, 31)
            },
            {
                'name': '2017-2018',
                'date_start': date(2017, 11, 1),
                'date_end': date(2018, 10, 31)
            },
            {
                'name': '2018-2019',
                'date_start': date(2018, 11, 1),
                'date_end': date(2019, 10, 31)
            },
            {
                'name': '2019-2020',
                'date_start': date(2019, 11, 1),
                'date_end': date(2020, 10, 31)
            },
            {
                'name': '2020-2021',
                'date_start': date(2020, 11, 1),
                'date_end': date(2021, 10, 31)
            },
            {
                'name': '2021-2022',
                'date_start': date(2021, 11, 1),
                'date_end': date(2022, 10, 31)
            },
        )
        for period in periods:
            obj, created = SubsidyPeriod.objects.get_or_create(
                name=period['name'],
                defaults={
                    "date_start": period['date_start'],
                    "date_end": period['date_end'],
                },
            )
            if not created:
                obj.date_start = period['date_start']
                obj.date_end = period['date_end']
                obj.save()
            if created:
                msg = f"SubsidyPeriod {period['name']} did NOT exist and was" \
                      f" created."
            else:
                msg = f"SubsidyPeriod {period['name']} was already there."
            print(msg)

    @staticmethod
    def normalize_exports():
        print("Normalizing exports...")
        print("Cleaning up existing exports.")
        DataExports.objects.all().delete()

        periods = [
            SubsidyPeriod.objects.get(name="2019-2020"),
            SubsidyPeriod.objects.get(name="2020-2021"),
        ]
        exports = []
        for period in periods:
            exports.extend(
                [
                    {
                        'name': "Cofinançades",
                        'subsidy_period': period,
                        'function_name': 'export_cofunded',
                        'ignore_errors': True
                    },
                    {
                        'name': "Memòria dels acompanyaments en fitxer de text",
                        'subsidy_period': period,
                        'function_name': 'export_stages_descriptions',
                        'ignore_errors': True
                    },
                    {
                        'name': "Exportació justificació (Cercle = Organitzadora)",
                        'subsidy_period': period,
                        'function_name': 'export',
                        'ignore_errors': True
                    },
                    {
                        'name': "Exportació justificació (Cercle = Entitat)",
                        'subsidy_period': period,
                        'function_name': 'export_by_entity',
                        'ignore_errors': True
                    },
                    {
                        'name': "Exportació justificació en 2 itineraris (Cercle = Organitzadora)",
                        'subsidy_period': period,
                        'function_name': 'export_dos_itineraris',
                        'ignore_errors': True
                    },
                    {
                        'name': "Exportació justificació en 2 itineraris (Cercle = Entitat)",
                        'subsidy_period': period,
                        'function_name': 'export_dos_itineraris_by_entity',
                        'ignore_errors': True
                    },
                    {
                        'name': "Detall dels acompanyaments",
                        'subsidy_period': period,
                        'function_name': 'export_stages_details',
                        'ignore_errors': True
                    },
                    {
                        'name': "Resultats enquestes de satisfacció",
                        'subsidy_period': period,
                        'function_name': 'export_polls',
                        'ignore_errors': True
                    },
                ]
            )

        # Different exports since 2021-2022
        period = SubsidyPeriod.objects.get(name="2021-2022")
        exports.extend(
            [
                {
                    'name': "Memòria dels acompanyaments en fitxer de text",
                    'subsidy_period': period,
                    'function_name': 'export_stages_descriptions',
                    'ignore_errors': True
                },
                {
                    'name': "Exportació justificació",
                    'subsidy_period': period,
                    'function_name': 'export_service',
                    'ignore_errors': True
                },
                {
                    'name': "Exportació justificació en 2 itineraris",
                    'subsidy_period': period,
                    'function_name': 'export_dos_itineraris',
                    'ignore_errors': True
                },
                {
                    'name': "Resultats enquestes de satisfacció",
                    'subsidy_period': period,
                    'function_name': 'export_polls_by_services',
                    'ignore_errors': True
                },
            ]
        )
        for export in exports:
            print(f"Updating or creating {export['function_name']}")
            DataExports.objects.create(**export)
        print("Done!")

    @staticmethod
    def add_group_permissions():
        # base user
        group, created = Group.objects.get_or_create(name='Permisos base')
        add_thing = Permission.objects.filter(
            codename__in=['add_logentry', 'change_logentry', 'view_logentry', 'delete_logentry', 'view_permission',
                          'add_town', 'change_town', 'delete_town', 'view_town', 'add_user', 'change_user',
                          'view_user', ]
        )
        group.permissions.set(add_thing)
        group.save()
        print('Permisos del grup Permisos base actualitzats.')

        # formació / sessions
        group, created = Group.objects.get_or_create(name="Gestió d'accions i sessions")
        add_thing = Permission.objects.filter(
            codename__in=[
                'add_activity', 'change_activity', 'delete_activity', 'view_activity', 'add_course',
                'change_course', 'delete_course', 'view_course', 'add_courseplace', 'change_courseplace',
                'delete_courseplace', 'view_courseplace', 'view_entity', 'add_organizer',
                'change_organizer', 'delete_organizer', 'view_organizer', 'add_attachment',
                'change_attachment', 'delete_attachment', 'view_attachment', 'add_source',
                'change_source', 'delete_source', 'view_source', 'add_thumbnail', 'change_thumbnail',
                'delete_thumbnail', 'view_thumbnail', 'add_thumbnaildimensions',
                'change_thumbnaildimensions', 'delete_thumbnaildimensions', 'view_thumbnaildimensions',
                'view_activityenrolled', 'delete_activityenrolled', 'change_activityenrolled', 'add_activityenrolled',
                'view_activityresourcefile', 'delete_activityresourcefile', 'change_activityresourcefile', 'add_activityresourcefile',
                'view_activitypoll',
            ]
        )
        group.permissions.set(add_thing)
        group.save()
        print("Permisos del grup Gestió d'accions i sessions actualitzats.")

        # projectes
        group, created = Group.objects.get_or_create(name='Gestió de projectes')
        add_thing = Permission.objects.filter(
            codename__in=[
                # Projectes
                'add_project', 'change_project', 'view_project',
                # Justificacions d'acompanyament
                'add_projectstagetype', 'change_projectstagetype', 'delete_projectstagetype', 'view_projectstagetype', 'view_projectstagetype',
                'add_projectstage', 'change_projectstage', 'delete_projectstage', 'view_projectstage',
                'add_projectstagesession', 'change_projectstagesession', 'delete_projectstagesession', 'view_projectstagesession',
                # Insercions laborals
                'add_employmentinsertion', 'change_employmentinsertion', 'delete_employmentinsertion', 'view_employmentinsertion',
                # Seguiment de projectes
                'view_projectsconstituted', 'view_projectsfollowup',
                # Etiquetes
                'add_tagulous_project_tags', 'change_tagulous_project_tags', 'delete_tagulous_project_tags', 'view_tagulous_project_tags',
                # Fitxers
                'add_projectfile', 'change_projectfile', 'delete_projectfile', 'view_projectfile',
            ]
        )
        group.permissions.set(add_thing)
        group.save()
        print("Permisos del grup Gestió de projectes actualitzats.")

        # exportacions
        group, created = Group.objects.get_or_create(name='Exportar justificació')
        add_thing = Permission.objects.filter(
            codename__in=['view_dataexports', ]
        )
        group.permissions.set(add_thing)
        group.save()
        print('Permisos del grup Exportar justificació actualitzats.')

        # gestió de sales
        group, created = Group.objects.get_or_create(name="Afegir o modificar Sales")
        add_thing = Permission.objects.filter(
            codename__in=['add_room', 'change_room', 'delete_room', ]
        )
        group.permissions.set(add_thing)
        group.save()
        print('Permisos del grup Afegir o modificar Sales actualitzats.')

        # gestió de reserves de sales
        group, created = Group.objects.get_or_create(name="Fer i modificar reserves d'espais")
        add_thing = Permission.objects.filter(
            codename__in=['add_reservation', 'change_reservation', 'delete_reservation', ]
        )
        group.permissions.set(add_thing)
        group.save()
        print('Permisos del grup Fer i modificar reserves d\'espais actualitzats.')

    def create_schedules(self):
        try:
            schedule(
                "apps.coopolis.tasks.mailqueue_send_command",
                name="send_queued_emails",
                schedule_type="I",
                minutes=1,
            )
            self.stdout.write(
                "CREADA: Tasca de django-q per l'enviament dels correus de la cua."
            )
        except IntegrityError:
            self.stdout.write(
                "JA EXISTENT: Tasca de django-q per l'enviament dels correus "
                "de la cua."
            )
