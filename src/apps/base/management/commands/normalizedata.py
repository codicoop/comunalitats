from calendar import monthrange

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from datetime import date

from apps.dataexports.models import SubsidyPeriod, DataExports


class Command(BaseCommand):
    help = 'Normalizes the minimum common data that every instance should have.'

    def handle(self, *args, **options):
        self.normalize_permissions()
        self.normalize_subsidy_periods()
        # Disabled until exports are adapted and can be introduced:
        # self.normalize_exports()

    @staticmethod
    def normalize_subsidy_periods():
        periods = (
            {
                'name': 'Sense justificar',
                'date_start': date(1975, 1, 1),
                'date_end': date(1975, 1, 1),
            },
            {
                'name': '2022-2023',
                'date_start': date(2022, 3, 1),
                'date_end': date(2023, 2, monthrange(2022, 2)[1]),
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

        exports = []

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
                    'name': "Detall dels acompanyaments",
                    'subsidy_period': period,
                    'function_name': 'export_stages_details_services',
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

    def normalize_permissions(self):
        # Administradors
        permissions = {
            "constance": [
                "change_config", "view_config",
            ],
            "mailing_manager": [
                "view_mail",
            ],
            "mailqueue": [
                "view_attachment",
                "view_mailermessage",
            ],
            "auth": [
                "add_permission",
            ],
            "dataexports": [
                "change_subsidyperiod", "add_subsidyperiod",
            ],
            "cc_courses": [
                "add_courseplace",
                "add_entity",
            ],
            "cc_users": [
                "delete_tagulous_user_tags",
            ],
            "projects": [
                "delete_tagulous_project_tags",
            ],
        }

        group, created = Group.objects.get_or_create(
            name="Responsable de backoffice"
        )
        group.permissions.set(self._get_permissions(Permission, permissions))
        group.save()
        if created:
            print('Grup Administradors creat.')
        else:
            print('Grup Administradors ja existent, permisos actualitzats.')

        # Equip
        permissions = {
            "cc_users": [
                "view_user", "change_user", "add_user",
                "add_tagulous_user_tags", "change_tagulous_user_tags",
                "view_tagulous_user_tags",
            ],
            "towns": [
                "view_town",
            ],
            "polls": [
                "view_activitypoll",
            ],
            "cc_courses": [
                "view_courseplace", "change_courseplace",
                "view_entity", "change_entity",
                "view_organizer", "change_organizer",
                "view_course", "change_course", "add_course",
                "view_activity", "change_activity", "add_activity",
                "view_activityresourcefile", "change_activityresourcefile",
                "add_activityresourcefile", "delete_activityresourcefile",
                "view_activityenrolled", "change_activityenrolled",
                "add_activityenrolled", "delete_activityenrolled",
                "view_activityfile", "change_activityfile",
                "add_activityfile", "delete_activityfile",
            ],
            "dataexports": [
                "view_subsidyperiod",
                "view_dataexports",
            ],
            "facilities_reservations": [
                "view_room", "add_room", "change_room",
                "view_reservation", "add_reservation", "change_reservation",
                "delete_reservation",
            ],
            "admin": [
                "view_logentry",
            ],
            "auth": [
                "view_group",
            ],
            "projects": [
                "add_tagulous_projects_tags", "change_tagulous_projects_tags",
                "view_tagulous_projects_tags",
            ],
        }
        group, created = Group.objects.get_or_create(
            name="Equip"
        )
        group.permissions.set(self._get_permissions(Permission, permissions))
        group.save()
        if created:
            print("Grup Equip creat.")
        else:
            print('Grup Equip ja existent, permisos actualitzats.')

    def _get_permissions(self, permission_model, permissions_dict: dict):
        permissions = []
        for content_type__app_label, codenames in permissions_dict.items():
            permissions += permission_model.objects.filter(
                content_type__app_label=content_type__app_label,
                codename__in=codenames)
        return permissions
