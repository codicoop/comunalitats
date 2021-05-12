from cc_courses.models import Activity
from dataexports.exports.justification import ExportJustification
from django.conf import settings


class ExportJustificationCofunded(ExportJustification):
    """
    
    Exportació cofinançades
    
    """
    def export(self):
        self.export_manager.import_correlations(
            settings.BASE_DIR
            + "/../apps/dataexports/fixtures/correlations_2019.json")

        # Each function called here handles the creation of each worksheets
        self.export_actuacions()
        self.export_participants()

        return self.export_manager.return_document("cofinançades")

    def get_sessions_obj(self, for_minors=False):
        obj = Activity.objects.filter(
            date_start__range=self.export_manager.subsidy_period.range,
            cofunded__isnull=False
        )
        return obj
