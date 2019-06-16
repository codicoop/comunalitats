from coopolis.models import Project, ProjectStage, User
from cc_courses.models import Course, Activity
from dataexports.models import DataExportsCorrelation
from django.http import HttpResponseNotFound, HttpResponse
from openpyxl import Workbook
from datetime import datetime
from openpyxl.utils import get_column_letter


class ExportFunctions:
    workbook = Workbook()
    worksheet = workbook.active
    subsidy_period_range = None
    row_number = 1
    error_message = set()

    @classmethod
    def callmethod(cls, name):
        if hasattr(cls, name):
            return getattr(cls, name)()
        else:
            return cls.return_404("La funció especificada no existeix")

    @classmethod
    def return_document(cls, name):
        if len(cls.error_message) > 0:
            return cls.return_404()

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-{name}.xlsx'.format(
            date=datetime.now().strftime('%Y-%m-%d'), name=name,
        )
        cls.workbook.save(response)
        return response

    @classmethod
    def return_404(cls, message=""):
        """When the exported data has to fit a specific format, there
        are many cases in which we need to stop the generation and tell
        the user that something needs to be fixed.
        This will show a blank page with the message.
        """
        if message:
            cls.error_message.add(message)
        message = "<h1>Error al generar el document</h1>" + " ".join(cls.error_message)
        return HttpResponseNotFound(message)

    @classmethod
    def get_correlation(cls, correlated_field, original_data, subsidy_period=2019):
        """When exporting data, we might need to make the exported data
         fit specific requirements. For example, we store the field
         'axis' as 'A', 'B', but the strings we actually need to
         show are:
         'A) Diagnosi i visibilització', 'B) Creació i desenvolupament'

         We use the DataExportsCorrelation model to store this correla-
         tions.

        This function is a wrapper to get those.
        """
        # TODO: Que carregui els resultats en memòria per evitar mil queries?
        try:
            new_data = DataExportsCorrelation.objects.get(
                subsidy_period=subsidy_period, correlated_field=correlated_field,
                original_data=original_data).correlated_data
        except DataExportsCorrelation.DoesNotExist:
            cls.error_message.add(
                "<p>El document no s'ha pogut generar perquè s'ha intentat aplicar aquesta correlació:</p"
                "<ul><li>Convocatòria: {}</li><li>Camp: {}</li><li>Dada original: {}</li></ul>"
                "<p>Però no s'ha trobat.</p>".format(subsidy_period, correlated_field, original_data))
            return None
        return new_data

    @classmethod
    def export_actuacions_2018_2019(cls):
        # Tutorial: https://djangotricks.blogspot.com/2019/02/how-to-export-data-to-xlsx-files.html
        # Docs: https://openpyxl.readthedocs.io/en/stable/tutorial.html#create-a-workbook
        cls.worksheet.title = "Actuacions"
        cls.subsidy_period_range = ["2018-10-01", "2019-09-30"]

        cls.actuacions_2018_2019_columns()
        cls.actuacions_2018_2019_rows_activities()
        # Total Activities: cls.row_number-1
        cls.actuacions_2018_2019_rows_stages()
        # Total Stages: cls.row_number-Total Activities-1
        return cls.return_document("actuacions")

    @classmethod
    def actuacions_2018_2019_columns(cls):
        columns = [
            ("Eix", 40),
            ("Tipus d'actuació", 70),
            ("Nom de l'actuació", 70),
            ("Data inici d'actuació", 16),
            ("Municipi", 30),
            ("Nombre de participants", 20),
            ("Material de difusió (S/N)", 21),
            ("Incidències", 20)
        ]

        # Assign the titles for each cell of the header
        for col_num, (column_title, column_width) in enumerate(columns, 1):
            cell = cls.worksheet.cell(row=1, column=col_num)
            cell.value = column_title
            column_letter = get_column_letter(col_num)
            column_dimensions = cls.worksheet.column_dimensions[column_letter]
            column_dimensions.width = column_width

    @classmethod
    def actuacions_2018_2019_rows_activities(cls):
        obj = Activity.objects.filter(justification="A", date_start__range=cls.subsidy_period_range)
        for item in obj:
            cls.row_number += 1

            # Define the data for each cell in the row
            if not item.axis:
                item.axis = "B"
            row = [
                cls.get_correlation("axis", item.axis),
                "B) Tallers sensibilització o dinamització",  # idem
                item.name,
                item.date_start,
                "BARCELONA",
                item.enrolled.count(),
                "No",
                ""
            ]
            for col_num, cell_value in enumerate(row, 1):
                cell = cls.worksheet.cell(row=cls.row_number, column=col_num)
                cell.value = cell_value

    @classmethod
    def actuacions_2018_2019_rows_stages(cls):
        obj = ProjectStage.objects.filter(subsidy_period=2019)
        for item in obj:
            cls.row_number += 1

            # Define the data for each cell in the row
            if not item.axis:
                item.axis = "B"
            row = [
                cls.get_correlation("axis", item.axis),
                "B) Acompanyament a empreses i entitats",  # Dada: stage_type. Pendent de saber correlacions.
                item.project.name,
                item.date_start,
                "BARCELONA",
                item.involved_partners.count(),
                "No",
                ""
            ]
            for col_num, cell_value in enumerate(row, 1):
                cell = cls.worksheet.cell(row=cls.row_number, column=col_num)
                cell.value = cell_value
