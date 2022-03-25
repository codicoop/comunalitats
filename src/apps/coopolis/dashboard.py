"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'Coopolis.back-office.dashboard.CustomIndexDashboard'
"""

from grappelli.dashboard import modules, Dashboard
from django.conf import settings
from django.urls import reverse
from constance import config


class MyDashboard(Dashboard):
    title = "Back-office de "+settings.PROJECT_NAME  # Aquest títol no l'està mostrant enlloc.

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # There's not a special reason for it to be here, just that it doesn't need the context.
        # move it to init_with_context safely if you want to!
        self.children.append(modules.RecentActions(
            title='Accions que has fet recentment',
            column=2,
            limit=5,
        ))

    def init_with_context(self, context):
        # 'Disabling' reservations module by default, by assigning an empty link module:
        reservations_module_app = modules.LinkList()
        reservations_module_calendar = modules.LinkList()
        if config.ENABLE_ROOM_RESERVATIONS_MODULE:
            reservations_module_app = modules.ModelList(
                    title="Gestió de reserves d'aules i sales",
                    column=1,
                    collapsible=False,
                    models=('apps.facilities_reservations.models.Reservation', 'apps.facilities_reservations.models.Room'),
                )
            reservations_module_calendar = modules.LinkList(
                    title="Calendari de reserves",
                    column=1,
                    collapsible=False,
                    children=(
                        {
                            'title': 'Obrir el calendari (pestanya nova)',
                            'url': reverse('fullcalendar'),
                            'external': False,
                            'target': True,
                        },
                    ),
                )

        group_children = [
            modules.ModelList(
                title='Accions i sessions',
                column=1,
                collapsible=False,
                models=('apps.cc_courses.models.Course', 'apps.cc_courses.models.Activity',),
            ),
            modules.ModelList(
                title='Acompanyament de projectes',
                column=1,
                collapsible=False,
                models=('apps.coopolis.models.projects.Project', 'apps.coopolis.models.projects.ProjectStage',
                        'apps.coopolis.models.projects.EmploymentInsertion', ),
            ),
            modules.ModelList(
                title='Seguiment de projectes',
                column=1,
                collapsible=False,
                models=(
                    'apps.coopolis.models.projects.ProjectsFollowUpService',
                    'apps.coopolis.models.projects.ProjectsConstitutedService',
                    'apps.coopolis.models.projects.ProjectsFollowUp',
                    'apps.coopolis.models.projects.ProjectsConstituted',
                ),
            ),
            reservations_module_app,
            reservations_module_calendar,
            modules.ModelList(
                title="Gestió d'usuàries",
                column=1,
                collapsible=False,
                models=('apps.coopolis.models.users.User',),
            ),
            modules.ModelList(
                title="Exportació de dades per justificacions",
                column=1,
                collapsible=False,
                models=('apps.dataexports.models.DataExports', 'apps.dataexports.models.SubsidyPeriod'),
            ),
            modules.ModelList(
                title="Gestió de dades",
                column=1,
                collapsible=False,
                models=('apps.cc_courses.models.Entity', 'apps.cc_courses.models.CoursePlace'),
            ),
        ]

        if context['request'].user.is_superuser:
            group_children.append(
                modules.ModelList(
                    title="Configuració dels correus electrònics",
                    column=1,
                    collapsible=False,
                    models=('mailing_manager.models.Mail',),
                )
            )

        self.children.append(modules.Group(
            title=settings.PROJECT_NAME,
            column=1,
            collapsible=True,
            children=group_children
        ))

        links_children = [
            ["Documentació", 'docs/'],
        ]
        if context['request'].user.is_superuser:
            links_children.append(['Gestió de textos del back-office', 'constance/config'])
            links_children.append(["Registre d'e-mails enviats", 'mailqueue/mailermessage/'])
            links_children.append(["Django-Q scheduling", 'django_q/'])
            links_children.append(["Registre d'activitat al panell d'administració", 'admin/logentry/'])

        self.children.append(modules.LinkList(
            title='Enllaços',
            column=3,
            children=links_children
        ))
