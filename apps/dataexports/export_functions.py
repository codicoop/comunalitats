from coopolis.models import Project, ProjectStage, User
from cc_courses.models import Course, Activity
from dataexports.models import DataExportsCorrelation
from django.http import HttpResponseNotFound, HttpResponse
from openpyxl import Workbook
from datetime import datetime
from openpyxl.utils import get_column_letter


class ExportFunctions:

    @staticmethod
    def callmethod(name):
        if hasattr(ExportFunctions, name):
            return getattr(ExportFunctions, name)()
        else:
            return HttpResponseNotFound("La funció especificada no existeix")

    @staticmethod
    def export_actuacions_2018_2019():
        # Tutorial: https://djangotricks.blogspot.com/2019/02/how-to-export-data-to-xlsx-files.html
        # Docs: https://openpyxl.readthedocs.io/en/stable/tutorial.html#create-a-workbook
        wb = Workbook()
        worksheet = wb.active
        worksheet.title = "Actuacions"

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
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, (column_title, column_width) in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title
            column_letter = get_column_letter(col_num)
            column_dimensions = worksheet.column_dimensions[column_letter]
            column_dimensions.width = column_width

        obj = Activity.objects.filter(justification="A", date_start__range=["2018-10-01", "2019-09-30"])
        for item in obj:
            row_num += 1
            # Hem de recordar que segons aquest ordre es defineixen els números de referència autoincrementals.
            # Per tant realment hauria de ser un sol excel amb diferents tabs per evitar problemes d'inconsistència
            # de dades.
            # Ojo que comença pel nº 2, perquè la 1a fila son els títols!!!

            # Define the data for each cell in the row
            if not item.axis:
                item.axis = "B"
            row = [
                DataExportsCorrelation.objects.get(
                    subsidy_period=2019, correlated_field="Eix", original_data=item.axis).correlated_data,
                "B) Tallers sensibilització o dinamització",  # idem
                item.name,
                item.date_start,
                "BARCELONA",
                item.enrolled.count(),
                "No",
                ""
            ]
            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-actuacions.xlsx'.format(
            date=datetime.now().strftime('%Y-%m-%d'),
        )
        wb.save(response)
        return response
