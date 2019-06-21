from coopolis.models import ProjectStage, Project, User
from cc_courses.models import Activity
from dataexports.models import DataExportsCorrelation, DataExports
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
    ignore_errors = False
    workbook = Workbook()
    worksheet = workbook.active
    subsidy_period = 2019

    # TODO: Passar això a una funció get_stages_obj
    stages_obj = ProjectStage.objects.filter(subsidy_period=subsidy_period).annotate(dcount=Count('project'))

    subsidy_period_range = None
    row_number = 1
    error_message = set()
    number_of_activities = 0
    number_of_stages = 0
    number_of_nouniversitaris = 0

    @classmethod
    def callmethod(cls, name):
        if hasattr(cls, name):
            obj = DataExports.objects.get(function_name=name)
            cls.ignore_errors = obj.ignore_errors
            cls.subsidy_period = obj.subsidy_period
            return getattr(cls, name)()
        else:
            return cls.return_404("La funció especificada no existeix")

    @classmethod
    def return_document(cls, name):
        if len(cls.error_message) > 0 and cls.ignore_errors is False:
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
    def get_sessions_obj(cls, justification="A", for_minors=False):
        return Activity.objects.filter(justification=justification, date_start__range=cls.subsidy_period_range,
                                       for_minors=for_minors)

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
        cls.export_founded_projects_2018_2019()
        cls.export_participants_2018_2019()
        cls.export_nouniversitaris_2018_2019()

        return cls.return_document("justificació2018-2019")

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
        cls.actuacions_2018_2019_rows_nouniversitaris()
        # Total Stages: cls.row_number-Total Activities-1

    @classmethod
    def actuacions_2018_2019_rows_activities(cls):
        obj = cls.get_sessions_obj()
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
        cls.number_of_stages = len(cls.stages_obj)
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
    def actuacions_2018_2019_rows_nouniversitaris(cls):
        obj = cls.get_sessions_obj(for_minors=True)
        cls.number_of_nouniversitaris = len(obj)
        for item in obj:
            cls.row_number += 1

            if not item.axis:
                item.axis = "E"
            row = [
                cls.get_correlation("axis", item.axis),
                "E) Tallers a joves",  # idem
                item.name,
                item.date_start,
                "BARCELONA",
                item.minors_participants_number,
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
                "",  # Camp no editable, l'ha d'omplir l'excel automàticament.
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

    @classmethod
    def export_founded_projects_2018_2019(cls):
        cls.worksheet = cls.workbook.create_sheet("EntitatCreada")
        cls.row_number = 1

        columns = [
            ("Referència", 10),
            ("Nom actuació", 40),
            ("Nom de l'entitat", 40),
            ("NIF de l'entitat", 12),
            ("Nom i cognoms persona de contacte", 30),
            ("Correu electrònic", 12),
            ("Telèfon", 10),
            ("Economia solidària (S/N)", 10),
        ]
        cls.create_columns(columns)

        cls.founded_projects_2018_2019_rows()

    @classmethod
    def founded_projects_2018_2019_rows(cls):
        obj = Project.objects.filter(constitution_date__range=cls.subsidy_period_range)
        for item in obj:
            cls.row_number += 1
            if item.cif is None:
                cls.error_message.add("<p><strong>Error: falta NIF</strong>. L'entitat '{}' apareix com a EntitatCreada"
                                      " perquè té una Data de constitució dins de la convocatòria, però si no té NIF, "
                                      "no pot ser inclosa a l'excel.</p>".format(item.name))
            row = [
                "",  # Referència. En aquest full no cal que tinguin relació amb Actuacions.
                "",  # Nom de l'actuació. Camp automàtic de l'excel.
                item.name,
                item.cif,
                item.partners.all()[0].full_name,
                item.mail,
                item.phone,
                "Sí"
            ]
            cls.fill_row_data(row)

    @classmethod
    def export_participants_2018_2019(cls):
        cls.worksheet = cls.workbook.create_sheet("Participants")
        cls.row_number = 1

        columns = [
            ("Referència", 10),
            ("Nom actuació", 40),
            ("Cognoms", 20),
            ("Nom", 10),
            ("Doc. identificatiu", 12),
            ("Gènere", 10),
            ("Data naixement", 10),
            ("Municipi del participant", 20),
        ]
        cls.create_columns(columns)

        cls.participants_2018_2019_rows()

    @classmethod
    def participants_2018_2019_rows(cls):
        activity_reference_number = 0
        obj = cls.get_sessions_obj(for_minors=False)
        for activity in obj:
            activity_reference_number += 1  # We know that activities where generated first, so it starts at 1.
            for participant in activity.enrolled.all():
                cls.row_number += 1
                gender = cls.get_correlation('gender', participant.gender)
                if gender is None:
                    cls.error_message.add(
                        "<p><strong>Error:</strong> la persona {} ha seleccionat un gènere que no és Home o Dona. "
                        "però la Generalitat només accepta que introduïm una d'aquestes dues opcions.".format(
                            participant.full_name))
                if participant.town is None:
                    town = ""
                    cls.error_message.add(
                        "<p><strong>Error:</strong> la persona {} no té cap població especificada. No es poden inserir a "
                        "l'excel de Participants cap persona que no inclogui la població.".format(
                            participant.full_name))
                else:
                    town = participant.town.name
                row = [
                    activity_reference_number,  # Referència.
                    "",  # Nom de l'actuació. Camp automàtic de l'excel.
                    participant.surname,
                    participant.first_name,
                    participant.id_number,
                    gender,
                    participant.birthdate,
                    town
                ]
                cls.fill_row_data(row)

    @classmethod
    def export_nouniversitaris_2018_2019(cls):
        cls.worksheet = cls.workbook.create_sheet("ParticipantsNoUniversitaris")
        cls.row_number = 1

        columns = [
            ("Referència", 10),
            ("Nom actuació", 40),
            ("Grau d'estudis", 20),
            ("Nom centre educatiu", 20),
        ]
        cls.create_columns(columns)

        cls.nouniversitaris_2018_2019_rows()

    @classmethod
    def nouniversitaris_2018_2019_rows(cls):
        nouniversitari_reference_number = cls.number_of_stages + cls.number_of_activities
        obj = cls.get_sessions_obj(for_minors=True)
        for activity in obj:
            cls.row_number += 1
            nouniversitari_reference_number += 1
            row = [
                nouniversitari_reference_number,  # Referència.
                "",  # Nom de l'actuació. Camp automàtic de l'excel.
                cls.get_correlation('minors_grade', activity.minors_grade),
                activity.minors_school_name,
            ]
            cls.fill_row_data(row)
