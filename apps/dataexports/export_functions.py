from coopolis.models import ProjectStage, Project, User, EmploymentInsertion
from cc_courses.models import Activity
from dataexports.models import DataExports
from django.http import HttpResponseNotFound, HttpResponse
from openpyxl import Workbook
from datetime import datetime
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Side, PatternFill, colors
from django.db.models import Count
import json
from django.conf import settings


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

    To use them, call callmethod('function_name')
    """

    def __init__(self):
        self.ignore_errors = False
        self.workbook = None
        self.worksheet = None
        self.subsidy_period = 2019

        self.stages_obj = None

        self.subsidy_period_range = None
        self.row_number = 1
        self.error_message = set()
        self.number_of_activities = 0
        self.number_of_stages = 0
        self.number_of_nouniversitaris = 0
        self.number_of_founded_projects = 0

        self.correlations = dict()

    def callmethod(self, name):
        if hasattr(self, name):
            obj = DataExports.objects.get(function_name=name)
            self.ignore_errors = obj.ignore_errors
            self.subsidy_period = obj.subsidy_period
            self.workbook = Workbook()
            self.worksheet = self.workbook.active
            return getattr(self, name)()
        else:
            return self.return_404("La funció especificada no existeix")

    def return_document(self, name):
        """ Attention: non-ascii characters in the name will cause
        an encoding error with gunicorn.
        Haven't tried it with a proxy under apache, in theory should
        work."""
        if len(self.error_message) > 0 and self.ignore_errors is False:
            return self.return_404()

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-{name}.xlsx'.format(
            date=datetime.now().strftime('%Y-%m-%d'), name=name,
        )
        self.workbook.save(response)
        return response

    def return_404(self, message=""):
        """When the exported data has to fit a specific format, there
        are many cases in which we need to stop the generation and tell
        the user that something needs to be fixed.
        This will show a blank page with the message.
        """
        if message:
            self.error_message.add(message)
        message = "<h1>Error al generar el document</h1>" + " ".join(self.error_message)
        return HttpResponseNotFound(message)

    def get_sessions_obj(self, justification="A", for_minors=False):
        return Activity.objects.filter(justification=justification, date_start__range=self.subsidy_period_range,
                                       for_minors=for_minors)

    def import_correlations(self, file_path):
        try:
            file_object = open(file_path, 'r')
            self.correlations = json.load(file_object)
        except FileNotFoundError:
            print(file_path + " not found. ")

    def get_correlation(self, correlated_field, original_data, subsidy_period=2019):
        """When exporting data, we might need to make the exported data
         fit specific requirements. For example, we store the field
         'axis' as 'A', 'B', but the strings we actually need to
         show are:
         'A) Diagnosi i visibilització', 'B) Creació i desenvolupament'

         We have these correlations in a json file and loaded at self.correlations.

        This function is a wrapper to get those.
        """
        try:
            new_data = self.correlations[correlated_field][original_data]
        except KeyError:
            self.error_message.add(
                "<p>El document no s'ha pogut generar perquè s'ha intentat aplicar aquesta correlació:</p"
                "<ul><li>Convocatòria: {}</li><li>Camp: {}</li><li>Dada original: {}</li></ul>"
                "<p>Però no s'ha trobat.</p>".format(subsidy_period, correlated_field, original_data))
            return None
        return new_data

    def create_columns(self, columns):
        """ create_columns

        Expects an iterable containing tuples with the name and the
        width of each column, like this:
        columns = [
            ("First", 40),
            ("Second", 70),
        ]
        """
        for col_num, (column_title, column_width) in enumerate(columns, 1):
            cell = self.worksheet.cell(row=1, column=col_num)
            column_letter = get_column_letter(col_num)
            column_dimensions = self.worksheet.column_dimensions[column_letter]
            column_dimensions.font = Font(name="ttf-opensans", size=9)
            column_dimensions.width = column_width
            cell.font = Font(bold=True, name="ttf-opensans", size=9)
            cell.border = Border(bottom=Side(border_style="thin", color='000000'))
            cell.value = str(column_title)

    def fill_row_data(self, row):
        """ fill_row_data

        Populates the columns of a given row with each of the values.
        Expects an iterable with the data for each row:
        row = [
            "first value",
            "second value",
        ]

        Optionally, values can be a tuple to mark the cell as error.
        That will fill the cell with red.
        row = [
            "first value",
            ("second value", True),
        ]
        """
        for col_num, cell_value in enumerate(row, 1):
            cell = self.worksheet.cell(row=self.row_number, column=col_num)
            if isinstance(cell_value, tuple):
                error_mark = cell_value[1]
                if error_mark:
                    cell.fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
                cell_value = cell_value[0]
            cell.value = str(cell_value)

    def export_2018_2019(self):
        self.import_correlations(settings.BASE_DIR + "/../apps/dataexports/fixtures/correlations_2019.json")
        self.subsidy_period_range = ["2018-11-01", "2019-10-31"]

        """ Each function here called handles the creation of one of the worksheets."""
        self.export_actuacions_2018_2019()
        self.export_stages_2018_2019()
        self.export_founded_projects_2018_2019()
        self.export_participants_2018_2019()
        self.export_nouniversitaris_2018_2019()
        self.export_insercionslaborals_2018_2019()

        return self.return_document("justificacio2018-2019")

    def export_2019_2020(self):
        self.import_correlations(settings.BASE_DIR + "/../apps/dataexports/fixtures/correlations_2019.json")
        self.subsidy_period_range = ["2019-11-01", "2020-10-31"]

        """ Each function here called handles the creation of one of the worksheets."""
        self.export_actuacions_2018_2019()
        self.export_stages_2018_2019()
        self.export_founded_projects_2018_2019()
        self.export_participants_2018_2019()
        self.export_nouniversitaris_2018_2019()
        self.export_insercionslaborals_2018_2019()

        return self.return_document("justificacio2018-2019")

    def export_actuacions_2018_2019(self):
        # Tutorial: https://djangotricks.blogspot.com/2019/02/how-to-export-data-to-xlsx-files.html
        # Docs: https://openpyxl.readthedocs.io/en/stable/tutorial.html#create-a-workbook
        self.worksheet.title = "Actuacions"

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
        self.create_columns(columns)
        self.actuacions_2018_2019_rows_activities()
        self.actuacions_2018_2019_rows_stages()
        self.actuacions_2018_2019_rows_nouniversitaris()
        self.actuacions_2018_2019_rows_founded_projects()
        # Total Stages: self.row_number-Total Activities-1

    def actuacions_2018_2019_rows_activities(self):
        obj = self.get_sessions_obj()
        self.number_of_activities = len(obj)
        for item in obj:
            self.row_number += 1

            axis = self.get_correlation("axis", item.axis)
            if axis is None:
                axis = ("", True)
            subaxis = self.get_correlation("subaxis", item.subaxis)
            if subaxis is None:
                subaxis = ("", True)
            town = None
            if item.place is not None:
                town = item.place.town
            if town is None or town == "":
                town = ("", True)
            row = [
                axis,
                subaxis,
                item.name,
                item.date_start,
                town,
                item.enrolled.count(),
                "No",
                ""
            ]
            self.fill_row_data(row)

    def actuacions_2018_2019_rows_stages(self):
        self.stages_obj = ProjectStage.objects.filter(
            subsidy_period=self.subsidy_period).annotate(dcount=Count('project'))
        self.number_of_stages = len(self.stages_obj)
        for item in self.stages_obj:
            self.row_number += 1

            axis = self.get_correlation("axis", item.axis)
            if axis is None:
                axis = ("", True)
            subaxis = self.get_correlation("subaxis", item.subaxis)
            if subaxis is None:
                subaxis = ("", True)
            town = item.project.town
            if town is None or town == "":
                town = ("", True)
            row = [
                axis,
                subaxis,
                item.project.name,
                item.date_start,
                town,
                item.involved_partners.count(),
                "No",
                ""
            ]
            self.fill_row_data(row)

    def actuacions_2018_2019_rows_nouniversitaris(self):
        obj = self.get_sessions_obj(for_minors=True)
        self.number_of_nouniversitaris = len(obj)
        for item in obj:
            self.row_number += 1

            axis = self.get_correlation("axis", item.axis)
            if axis is None:
                axis = ("", True)
            subaxis = self.get_correlation("subaxis", item.subaxis)
            if subaxis is None:
                subaxis = ("", True)
            town = None
            if item.place is not None:
                town = item.place.town
            if town is None or town == "":
                town = ("", True)
            row = [
                axis,
                subaxis,
                item.name,
                item.date_start,
                town,
                item.minors_participants_number,
                "No",
                ""
            ]
            self.fill_row_data(row)

    def actuacions_2018_2019_rows_founded_projects(self):
        """
        Tots els projectes que tinguin data de constitució dins de les dates de la convocatòria apareixeran
        a la pestanya d'EntitatsCreades.
        No obstant només aquells que tinguin una actuació vinculada durant el període de la convocatòria han de
        d'aparèixer a la pestanya d'Actuacions.

        Els que tenen això vol dir que hi ha hagut un acompanyament del projecte dins de la convocatòria.
        Poden haver-hi hagut varis acompanyaments, per tant, hem de d'obtenir l'acompanyament més recent.

        Si tot això existeix mostrem les dades del més recent, sinó, ignorem el projecte.

        Després a la pestanya d'EntitatsCreades hem de fer el mateix filtre per saber quins tenen
        actuació creada, i deduïr per l'ordre quina ID li toca.
        """
        obj = Project.objects.filter(constitution_date__range=self.subsidy_period_range)
        self.number_of_founded_projects = len(obj)
        for project in obj:
            stages = ProjectStage.objects.filter(
                project=project, subsidy_period=self.subsidy_period
            ).order_by("-date_start")[:1]
            if stages.count() < 1:
                continue
            stage = stages.all()[0]

            self.row_number += 1
            axis = self.get_correlation("axis", stage.axis)
            if axis is None:
                axis = ("", True)
            subaxis = self.get_correlation("subaxis", stage.subaxis)
            if subaxis is None:
                subaxis = ("", True)
            town = project.town
            if town is None or town == "":
                town = ("", True)
            row = [
                axis,
                subaxis,
                project.name,
                stage.date_start,
                town,
                stage.involved_partners.count(),
                "No",
                ""
            ]
            self.fill_row_data(row)

    def export_stages_2018_2019(self):
        self.worksheet = self.workbook.create_sheet("Acompanyaments")
        self.row_number = 1

        columns = [
            ("Referència", 20),
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
        self.create_columns(columns)

        self.stages_2018_2019_rows()

    def stages_2018_2019_rows(self):
        reference_number = self.number_of_activities
        for item in self.stages_obj:
            self.row_number += 1
            reference_number += 1
            hours = item.hours if item.hours is not None else ("", True)
            town = item.project.town if item.project.town is not None else ("", True)
            row = [
                f"{reference_number} {item.project.name}",  # Referència.
                item.project.name,  # Camp no editable, l'ha d'omplir l'excel automàticament.
                ("Entitat", True),
                # "Destinatari de l'actuació" Opcions: Persona física/Promotor del projecte/Entitat PENDENT.
                item.project.name,  # "En cas d'entitat (Nom de l'entitat)"
                ("Constituida", True),  # "En cas d'entitat" Opcions: Constituida/En procés/No finalitzat. PENDENT.
                self.get_correlation("stage_type", item.stage_type),  # "Creació/consolidació".
                item.date_start,
                town,
                item.project.object_finality,  # Breu descripció.
                hours  # Total hores d'acompanyament.
            ]
            self.fill_row_data(row)

    def export_founded_projects_2018_2019(self):
        self.worksheet = self.workbook.create_sheet("EntitatCreada")
        self.row_number = 1

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
        self.create_columns(columns)

        self.founded_projects_2018_2019_rows()

    def founded_projects_2018_2019_rows(self):
        # The Ids start at 1, so later we add 1 to this number to have the right ID.
        founded_projects_reference_number = \
            self.number_of_stages + self.number_of_activities + self.number_of_nouniversitaris
        obj = Project.objects.filter(constitution_date__range=self.subsidy_period_range)
        for project in obj:
            # Repeating the same filter than in Actuacions to determine if we have an Actuació or not
            reference_number = ""
            name = ""
            stages = ProjectStage.objects.filter(
                project=project, subsidy_period=self.subsidy_period
            ).order_by("-date_start")[:1]
            if stages.count() > 0:
                stage = stages.all()[0]
                founded_projects_reference_number += 1
                reference_number = f"{founded_projects_reference_number} {project.name}"
                name = project.name

            self.row_number += 1
            if project.cif is None:
                self.error_message.add(
                    "<p><strong>Error: falta NIF</strong>. L'entitat '{}' apareix com a EntitatCreada"
                    " perquè té una Data de constitució dins de la convocatòria, però si no té NIF, "
                    "no pot ser inclosa a l'excel.</p>".format(project.name))
                project.cif = ""
            row = [
                reference_number,  # Referència. En aquest full no cal que tinguin relació amb Actuacions.
                name,  # Nom de l'actuació. En aquest full no cal que tinguin relació amb Actuacions.
                project.name,
                project.cif,
                project.partners.all()[0].full_name,
                project.mail,
                project.phone,
                "Sí"
            ]
            self.fill_row_data(row)

    def export_participants_2018_2019(self):
        self.worksheet = self.workbook.create_sheet("Participants")
        self.row_number = 1

        columns = [
            ("Referència", 40),
            ("Nom actuació", 40),
            ("Cognoms", 20),
            ("Nom", 10),
            ("Doc. identificatiu", 12),
            ("Gènere", 10),
            ("Data naixement", 10),
            ("Municipi del participant", 20),
            ("[Situació laboral]", 20),
            ("[Procedència]", 20),
            ("[Nivell d'estudis]", 20),
            ("[Com ens has conegut]", 20),
            ("[Organitzadora]", 30),
        ]
        self.create_columns(columns)

        self.participants_2018_2019_rows()

    def participants_2018_2019_rows(self):
        activity_reference_number = 0
        obj = self.get_sessions_obj(for_minors=False)
        for activity in obj:
            activity_reference_number += 1  # We know that activities where generated first, so it starts at 1.
            for participant in activity.enrolled.all():
                self.row_number += 1
                if participant.gender is None:
                    gender = ""
                else:
                    gender = self.get_correlation('gender', participant.gender)
                if participant.town is None:
                    town = ""
                else:
                    town = participant.town.name
                row = [
                    f"{activity_reference_number} {activity.name}",  # Referència.
                    activity.name,  # Nom de l'actuació. Camp automàtic de l'excel.
                    participant.surname,
                    participant.first_name,
                    participant.id_number,
                    gender,
                    participant.birthdate,
                    town,
                    participant.get_employment_situation_display() if participant.get_employment_situation_display() else "",
                    participant.get_birth_place_display() if participant.get_birth_place_display() else "",
                    participant.get_educational_level_display() if participant.get_educational_level_display() else "",
                    participant.get_discovered_us_display() if participant.get_discovered_us_display() else "",
                    activity.organizer if activity.organizer else "",
                ]
                self.fill_row_data(row)

    def export_nouniversitaris_2018_2019(self):
        self.worksheet = self.workbook.create_sheet("ParticipantsNoUniversitaris")
        self.row_number = 1

        columns = [
            ("Referència", 40),
            ("Nom actuació", 40),
            ("Grau d'estudis", 20),
            ("Nom centre educatiu", 20),
        ]
        self.create_columns(columns)

        self.nouniversitaris_2018_2019_rows()

    def nouniversitaris_2018_2019_rows(self):
        nouniversitari_reference_number = self.number_of_stages + self.number_of_activities
        obj = self.get_sessions_obj(for_minors=True)
        for activity in obj:
            self.row_number += 1
            nouniversitari_reference_number += 1
            row = [
                f"{nouniversitari_reference_number} {activity.name}",  # Referència.
                activity.name,  # Nom de l'actuació. Camp automàtic de l'excel.
                self.get_correlation('minors_grade', activity.minors_grade),
                activity.minors_school_name,
            ]
            self.fill_row_data(row)

    def export_insercionslaborals_2018_2019(self):
        self.worksheet = self.workbook.create_sheet("InsercionsLaborals")
        self.row_number = 1

        columns = [
            ("Projecte", 40),
            ("Persona", 40),
            ("Convocatòria", 20),
            ("Data alta SS", 20),
            ("Tipus de contracte", 20),
            ("Durada", 20),
        ]
        self.create_columns(columns)

        self.insercionslaborals_2018_2019_rows()

    def insercionslaborals_2018_2019_rows(self):
        obj = EmploymentInsertion.objects.filter(
            subsidy_period__date_start__range=self.subsidy_period_range)
        for insertion in obj:
            self.row_number += 1
            row = [
                insertion.project.name,  # Projecte
                insertion.user.full_name,  # Persona
                insertion.subsidy_period,  # Convocatòria
                insertion.insertion_date,  # Data d'alta SS
                insertion.get_contract_type_display(),  # Tipus de contracte
                insertion.get_duration_display(),  # Durada del contracte
            ]
            self.fill_row_data(row)
