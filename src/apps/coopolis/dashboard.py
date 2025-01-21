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

        group_children = [
            modules.ModelList(
                title='Projectes i activitats',
                column=1,
                collapsible=False,
                models=('apps.cc_courses.models.Course', 'apps.cc_courses.models.Activity',),
            ),
            modules.ModelList(
                title='Acompanyament de projectes',
                column=1,
                collapsible=False,
                models=(
                    'apps.projects.models.Project',
                    'apps.projects.models.ProjectStage',
                    'apps.projects.models.EmploymentInsertion',
                    'apps.projects.models.ProjectStageSession',
                ),
            ),
            modules.ModelList(
                title='Seguiment de projectes',
                column=1,
                collapsible=False,
                models=(
                    'apps.projects.models.ProjectsFollowUpService',
                    'apps.projects.models.ProjectsConstitutedService',
                ),
            ),
            modules.ModelList(
                title="Gestió de reserves d'aules i sales",
                column=1,
                collapsible=False,
                models=('apps.facilities_reservations.models.Reservation',
                        'apps.facilities_reservations.models.Room'),
            ),
            modules.LinkList(
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
            ),
            modules.ModelList(
                title="Gestió d'usuàries",
                column=1,
                collapsible=False,
                models=('apps.cc_users.models.User',),
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

        self.children.append(modules.Group(
            title=settings.PROJECT_NAME,
            column=1,
            collapsible=True,
            children=group_children
        ))

        self.children.append(
            modules.ModelList(
                "Paràmetres de l'aplicació",
                column=1,
                collapsible=False,
                models=(
                    "apps.base.models.Customization",
                    "constance.*",
                    "mailing_manager.*",
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                "Correus enviats",
                column=1,
                collapsible=False,
                models=("mailqueue.*",),
            )
        )

        links_children = [
        ]
        if context['request'].user.is_superuser:
            links_children.append(["Registre d'activitat al panell d'administració", 'admin/logentry/'])
            links_children.append(["Descàrrega de la base de dades de les 00:00", reverse('db_backup_download')])

        self.children.append(modules.LinkList(
            title='Enllaços',
            column=3,
            children=links_children
        ))
