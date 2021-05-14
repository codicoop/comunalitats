from coopolis.models import ProjectStage
from dataexports.exports.manager import ExcelExportManager


class ExportCovidHours:
    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_covid_stages()

        return self.export_manager.return_document("hores_covid")

    def export_covid_stages(self):
        self.export_manager.worksheet.title = "Acompanyaments covid"
        self.export_manager.row_number = 1

        columns = [
            ("Projecte", 20),
            ("Data d'inici", 20),
            ("Tipus d'acompanyament", 20),
            ("Responsable", 20),
            ("Número d'hores", 20),
            ("Eix-subeix", 20),
            ("Convocatòria", 20),
            ("Participants", 20),
            ("Ateneu/Cercle", 20),
        ]
        self.export_manager.create_columns(columns)

        self.covid_stages_rows()

    def get_stages_obj(self):
        return ProjectStage.objects.order_by('date_start').filter(
            subsidy_period=self.export_manager.subsidy_period,
            covid_crisis=True
        )

    def covid_stages_rows(self):
        stages_obj = self.get_stages_obj()

        for stage in stages_obj:
            self.export_manager.row_number += 1
            row = [
                stage.project.name,
                stage.date_start,
                stage.get_stage_type_display(),
                stage.stage_responsible,
                stage.hours_sum(),
                stage.axis_summary(),
                stage.subsidy_period,
                len(stage.involved_partners.all()),
                stage.stage_organizer,
            ]
            self.export_manager.fill_row_data(row)
