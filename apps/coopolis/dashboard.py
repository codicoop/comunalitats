"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'Coopolis.back-office.dashboard.CustomIndexDashboard'
"""

from grappelli.dashboard import modules, Dashboard


class MyDashboard(Dashboard):
    title = "Back-office de Coòpolis"
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(modules.LinkList(
            title='Enllaços',
            column=2,
            children=(
                {
                    'title': 'Python website',
                    'url': 'http://www.python.org',
                    'external': True,
                    'description': 'Python programming language rocks!',
                    'target': '_blank',
                },
                ['Django website', 'http://www.djangoproject.com', True],
                ['Some internal link', '/some/internal/link/'],
            )
        ))

        self.children.append(modules.RecentActions(
            title='Accions recents',
            column=3,
            limit=5,
        ))
