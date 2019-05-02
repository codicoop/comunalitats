"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'Coopolis.back-office.dashboard.CustomIndexDashboard'
"""

from grappelli.dashboard import modules, Dashboard


class MyDashboard(Dashboard):
    title = "Back-office de Coòpolis"  # Aquest títol no l'està mostrant enlloc.

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(modules.Group(
            title="Coòpolis",
            column=1,
            collapsible=True,
            children=[
                modules.ModelList(
                    title='Accions i sessions',
                    column=1,
                    collapsible=False,
                    models=('cc_courses.models.Course', 'cc_courses.models.Activity',),
                ),
                modules.ModelList(
                    title='Acompanyament de projectes',
                    column=1,
                    collapsible=False,
                    models=('coopolis.models.Project', 'coopolis.models.ProjectStage'),
                ),
                modules.ModelList(
                    title="Gestió d'usuàries",
                    column=1,
                    collapsible=False,
                    models=('coopolis.models.User', 'django.contrib.auth.models.Group',),
                ),
                modules.ModelList(
                    title="Gestió de dades",
                    column=1,
                    collapsible=False,
                    models=('cc_courses.models.Organizer', 'cc_courses.models.Entity', 'cc_courses.models.CoursePlace'),
                )
            ]
        ))

        self.children.append(modules.RecentActions(
            title='Accions que has fet recentment',
            column=2,
            limit=5,
        ))

        self.children.append(modules.LinkList(
            title='Enllaços',
            column=3,
            children=(
                ['Gestió de textos del back-office', 'constance/config'],
            )
        ))
