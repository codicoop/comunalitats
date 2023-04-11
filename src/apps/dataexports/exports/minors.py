from apps.cc_courses.models import Activity
from apps.coopolis.choices import ServicesChoices
from apps.dataexports.exports.manager import ExcelExportManager
from apps.projects.models import ProjectStage, Project, EmploymentInsertion


class ExportMinors:
    subsidy_period_str = "2022-23"

    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.number_of_nouniversitaris = 0

    def get_sessions_obj(self):
        return Activity.objects.filter(
            date_start__range=self.export_manager.subsidy_period.range,
            for_minors=True,
        )

    """
    
    Exportació Ateneu
    
    """
    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_actuacions()
        self.export_nouniversitaris()

        return self.export_manager.return_document("justificacio-menors")

    def export_actuacions(self):
        # Tutorial: https://djangotricks.blogspot.com/2019/02/how-to-export-
        # data-to-xlsx-files.html
        # Docs: https://openpyxl.readthedocs.io/en/stable/
        # tutorial.html#create-a-workbook
        self.export_manager.worksheet.title = "Actuacions"

        columns = [
            ("Servei", 40),
            ("Actuacions", 70),
            ("Nom de l'actuació", 70),
            ("Data inici d'actuació", 16),
            ("Període actuacions", 30),
            ("Municipi", 30),
            ("Material de difusió (S/N)", 21),
            ("Incidències", 20),
            ("[Document acreditatiu]", 21),
            ("[Entitat]", 20),
            ("[Lloc]", 20),
            ("[Acció]", 20),
        ]
        self.export_manager.create_columns(columns)
        self.actuacions_rows_nouniversitaris()
        # Total Stages: self.export_manager.row_number-Total Activities-1

    def actuacions_rows_nouniversitaris(self):
        obj = self.get_sessions_obj()
        self.number_of_nouniversitaris = len(obj)
        for item in obj:
            self.export_manager.row_number += 1

            service = item.get_service_display() if item.service else ""
            sub_service = item.get_sub_service_display() if item.sub_service else ""
            town = ("", True)
            if item.place and item.place.town:
                town = str(item.place.town)
            material_difusio = "No"
            if item.file1.name:
                material_difusio = "Sí"
            document_acreditatiu = "No"
            if item.photo2.name:
                document_acreditatiu = "Sí"

            row = [
                service,
                sub_service,
                item.name,
                item.date_start,
                "",  # Període
                town,
                material_difusio,
                "",  # Incidències
                document_acreditatiu,
                item.entities_str,  # Entitat
                str(item.place) if item.place else '',  # Lloc
                str(item.course),  # Acció
            ]
            self.export_manager.fill_row_data(row)

    def export_nouniversitaris(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet(
                "ParticipantsNoUniversitaris"
            )
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 40),
            ("Nom actuació", 40),
            ("Grau d'estudis", 20),
            ("Nom centre educatiu", 20),
        ]
        self.export_manager.create_columns(columns)

        self.nouniversitaris_rows()

    def nouniversitaris_rows(self):
        nouniversitari_reference_number = 0
        obj = self.get_sessions_obj()
        for activity in obj:
            self.export_manager.row_number += 1
            nouniversitari_reference_number += 1
            row = [
                self.get_formatted_reference(
                    self.export_manager.row_number,
                    activity.service,
                    activity.name,
                ),
                # Referència.
                activity.name,  # Nom de l'actuació. Camp automàtic de l'excel.
                self.export_manager.get_correlation(
                    'minors_grade', activity.minors_grade),
                activity.minors_school_name,
            ]
            self.export_manager.fill_row_data(row)

    def get_formatted_reference(
        self,
        ref_num,
        service_id,
        actuation_name,
        subsidy_period=None,
    ):
        # Format justificació 22-23:
        # 1 B) 2022-23 Nom de l'activitat
        if not service_id or not actuation_name:
            return "", True
        if not subsidy_period:
            subsidy_period = self.subsidy_period_str
        service_code = ServicesChoices(service_id).name
        return (
            f"{ref_num} {service_code}) {subsidy_period} {actuation_name}"
        )
