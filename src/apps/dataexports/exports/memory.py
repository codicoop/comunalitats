from apps.coopolis.models import ProjectStage
from django.http import HttpResponse
from django.db.models import Q

from apps.dataexports.exports.manager import ExportManager


class ExportMemory:
    """

    Exportació de les memòries d'acompanyament a fitxer de text

    """
    def __init__(self, export_obj):
        self.export_manager = ExportManager(export_obj)

    def export_stages_descriptions(self):
        qs = ProjectStage.objects.filter(
            Q(subsidy_period=self.export_manager.subsidy_period)
            and
            (
                (Q(cofunded__isnull=True))
                or
                (Q(cofunded__isnull=False) and Q(cofunded_ateneu=True))
            )
        )
        lines = []
        for stage in qs:
            lines.append(self._html_title(stage.project.name))
            for stage_session in stage.stage_sessions.all():
                if stage_session.follow_up:
                    lines.append(self._html_paragraph(stage_session.follow_up))
        return HttpResponse(self._compose_html(lines))

    @staticmethod
    def _compose_html(lines):
        html = "\r".join(lines)
        html = (
            "<em>Recorda! Fes ctrl+a o cmd+a per seleccionar-ho tot!</em>"
            + html
        )
        html = f"<body style=\"width: 800px\">{html}</body>"
        return html

    @staticmethod
    def _html_title(text):
        return f"<h1>{text}</h1>"

    @staticmethod
    def _html_paragraph(text):
        return f"<p>{text}</p>"
