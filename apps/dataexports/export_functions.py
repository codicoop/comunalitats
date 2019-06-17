from coopolis.models import ProjectStage
from cc_courses.models import Activity
from dataexports.models import DataExportsCorrelation
from django.http import HttpResponseNotFound, HttpResponse
from openpyxl import Workbook
from datetime import datetime
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Side
from django.db.models import Count


class ExportFunctions:
    """ExportFunctions

    This is the generation of excel-like data (in .xlsx) made to fit
    the official formats required for the justification of the
    subsidies.

    Given that each year it changes, and we might need multiple
    documents, or even each Ateneu might need a specific document
    for subsidies that are not the 'conveni', we created a simple
    system to create different functions, 'register' them in the
    admin, and launch them from there.

    This class holds the functions that generate this .xlsx.

    To use them, call ExportFunctions.callmethod('function_name')
    """
    workbook = Workbook()
    worksheet = workbook.active
    stages_obj = ProjectStage.objects.filter(subsidy_period=2019).annotate(dcount=Count('project'))
    subsidy_period_range = None
    row_number = 1
    error_message = set()
    number_of_activities = 0
    number_of_stages = 0

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
    def create_columns(cls, columns):
        """ create_columns

        Expects an iterable containing tuples with the name and the
        width of each column, like this:
        columns = [
            ("First", 40),
            ("Second", 70),
        ]
        """
        for col_num, (column_title, column_width) in enumerate(columns, 1):
            cell = cls.worksheet.cell(row=1, column=col_num)
            column_letter = get_column_letter(col_num)
            column_dimensions = cls.worksheet.column_dimensions[column_letter]
            column_dimensions.font = Font(name="ttf-opensans", size=9)
            column_dimensions.width = column_width
            cell.font = Font(bold=True, name="ttf-opensans", size=9)
            cell.border = Border(bottom=Side(border_style="thin", color='000000'))
            cell.value = column_title

    @classmethod
    def fill_row_data(cls, row):
        """ fill_row_data

        Populates the columns of a given row with each of the values.
        Expects an iterable with the data for each row:
        row = [
            "first value",
            "second value",
        ]
        """
        for col_num, cell_value in enumerate(row, 1):
            cell = cls.worksheet.cell(row=cls.row_number, column=col_num)
            cell.value = cell_value

    @classmethod
    def export_2018_2019(cls):
        """ Each function here called handles the creation of one of the worksheets."""
        cls.subsidy_period_range = ["2018-10-01", "2019-09-30"]

        cls.export_actuacions_2018_2019()
        cls.export_stages_2018_2019()

        return cls.return_document("actuacions")

    @classmethod
    def export_actuacions_2018_2019(cls):
        # Tutorial: https://djangotricks.blogspot.com/2019/02/how-to-export-data-to-xlsx-files.html
        # Docs: https://openpyxl.readthedocs.io/en/stable/tutorial.html#create-a-workbook
        cls.worksheet.title = "Actuacions"

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
        cls.create_columns(columns)
        cls.actuacions_2018_2019_rows_activities()
        cls.actuacions_2018_2019_rows_stages()
        # Total Stages: cls.row_number-Total Activities-1

    @classmethod
    def actuacions_2018_2019_rows_activities(cls):
        obj = Activity.objects.filter(justification="A", date_start__range=cls.subsidy_period_range)
        cls.number_of_activities = len(obj)
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
            cls.fill_row_data(row)

    @classmethod
    def actuacions_2018_2019_rows_stages(cls):
        for item in cls.stages_obj:
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
            cls.fill_row_data(row)

    @classmethod
    def export_stages_2018_2019(cls):
        cls.worksheet = cls.workbook.create_sheet("Acompanyaments")
        cls.row_number = 1

        columns = [
            ("Referència", 10),
            ("Nom actuació", 40),
            ("Destinatari de l'acompanyament", 28),
            ("En cas d'entitat (nom de l'entitat)", 40),
            ("En cas d'entitat", 16),
            ("Creació/consolidació", 18),
            ("Data d'inici", 13),
            ("Localitat", 20),
            ("Breu descripció del projecte", 50),
            ("Total hores d'acompanyament", 10),
        ]
        cls.create_columns(columns)

        cls.stages_2018_2019_rows()

    @classmethod
    def stages_2018_2019_rows(cls):
        reference_number = cls.number_of_activities
        for item in cls.stages_obj:
            cls.row_number += 1
            reference_number += 1
            if not item.axis:
                item.axis = "B"
            row = [
                reference_number,  # Referència.
                item.project.name,  # "Nom de l'actuació". Això és el nom del projecte?
                "destinatari?",  # "Destinatari de l'actuació" Opcions: Persona física/Promotor del projecte/Entitat <- d'on trec aquesta dada?
                item.project.name,  # "En cas d'entitat (Nom de l'entitat)" <- aquí repetim el nom del projecte?
                "Constituida",  # "En cas d'entitat" Opcions: Constituida/En procés/No finalitzat. Dada que ve del camp Estat del projecte.
                "Nova creació",  # "Creació/consolidació". Opcions: Nova creació/Creixement. Ve del camp Tipus d'acompanyament.
                item.date_start,
                "BARCELONA",
                item.project.object_finality,  # Breu descripció. Hi he posat el camp d'Objecte i finalitat. És OK?
                0  # Total hores d'acompanyament. <- aquí què hi va? no tenim aquesta dada.
            ]
            cls.fill_row_data(row)
