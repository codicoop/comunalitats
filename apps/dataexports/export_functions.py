from coopolis.models import Project, ProjectStage, User
from cc_courses.models import Course, Activity
from django.http import HttpResponseNotFound, HttpResponse
from openpyxl import Workbook
from datetime import datetime


class ExportFunctions:

    @staticmethod
    def callmethod(name):
        if hasattr(ExportFunctions, name):
            return getattr(ExportFunctions, name)()
        else:
            return HttpResponseNotFound("La funció especificada no existeix")

    @staticmethod
    def export_actuacions_2018_2019():
        wb = Workbook()
        worksheet = wb.active
        worksheet.title = "Actuacions"

        columns = [
            'Referència',
            "Eix",
            "Tipus d'actuació",
            "Nom de l'actuació",
            "Data inici d'actuació",
            "Municipi",
            "Nombre de participants",
            "Material de difusió (S/N)",
            "Incidències"
        ]
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title

        obj = Activity.objects.filter(justification="A", date_start__range=["2018-10-01", "2019-09-30"])
        for item in obj:
            row_num += 1

            # Define the data for each cell in the row
            row = [
                "",
                "A) Diagnosi i visibilització",  # s'ha de calcular l'Eix real
                "A) Reunions de la taula territorial",  # idem
                item.name,
                item.date_start,
                "BARCELONA",
                item.enrolled.count(),
                "No",
                ""
            ]

            # Assign the data for each cell of the row
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
