from apps.cc_courses.models import Activity
from apps.coopolis.choices import ServicesChoices
from apps.dataexports.exports.manager import ExcelExportManager
from apps.projects.models import EmploymentInsertion, Project, ProjectStage


class ExportJustificationService:
    subsidy_period_str = "2022-23"

    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.number_of_activities = 0
        self.number_of_stages = 0
        self.number_of_nouniversitaris = 0
        self.number_of_founded_projects = 0
        # Si a cada item del diccionari se li posa un nom diferent, agruparà
        # els diferents acompanyaments pel tipus d'acompanyament i per tant
        # apareixerà una línia nova per cada tipus d'acompanyament dins d'una
        # mateixa convocatòria.
        # Si en canvi es posen tots iguals, tipus:
        #         self.stages_groups = {
        #             11: 'creacio',
        #             12: 'creacio',
        #             13: 'creacio',
        #         }
        # Això farà que cada projecte només aparegui com a un sol acompanyament
        # independentment de que n'hagi tingut un de cada tipus.
        self.stages_groups = {
            11: "creacio",
            12: "consolidacio",
            13: "creixement",
        }
        self.stages_obj = None

    def get_sessions_obj(self):
        return Activity.objects.filter(
            date_start__range=self.export_manager.subsidy_period.range,
        )

    """
    
    Exportació Ateneu
    
    """

    def export(self):
        """Each function here called handles the creation of one of the
        worksheets."""
        self.export_actuacions()
        self.export_participants()
        self.export_insercionslaborals()
        self.export_stages()
        self.export_founded_projects()
        # A l'excel de justificació no hi ha la pestanya dels NoUniversitaris.
        # self.export_nouniversitaris()

        return self.export_manager.return_document("justificacio")

    def export_actuacions(self):
        # Tutorial: https://djangotricks.blogspot.com/2019/02/how-to-export-
        # data-to-xlsx-files.html
        # Docs: https://openpyxl.readthedocs.io/en/stable/
        # tutorial.html#create-a-workbook
        self.export_manager.worksheet.title = "Actuacions"

        columns = [
            ("Projecte al qual s'engloba", 40),
            ("Sector del projecte", 40),
            ("Nom de l'actuació", 40),
            ("Descripció actuació", 40),
            ("Tipus actuació", 40),
            ("Servei", 40),
            ("Actuacions", 70),
            ("Rol Comunalitat", 40),
            ("Treball en Xarxa", 40),
            ("Agents implicats", 40),
            ("Data inici d'actuació", 16),
            ("Període actuacions", 30),
            ("Municipi", 30),
            ("Barri", 30),
            ("Estimació hores dedicació", 20),
            ("Material de difusió (S/N)", 21),
            ("Incidències", 20),
            ("[Document acreditatiu]", 21),
            ("[Entitat]", 20),
            ("[Lloc]", 20),
            ("[Acció]", 20),
        ]
        self.export_manager.create_columns(columns)
        self.actuacions_rows_activities()
        self.actuacions_rows_stages()
        # self.actuacions_rows_nouniversitaris()
        self.actuacions_rows_founded_projects()
        # Total Stages: self.export_manager.row_number-Total Activities-1

    def actuacions_rows_activities(self):
        # Anteriorment, per una banda es mostràven totes les activitats que
        # no eren per menors i més avall en un altre bloc, les de menors.
        # Ara que una activitat pot tenir qualsevol de les dues coses juntes,
        # això genera problemes a l'hora de determinar quines han d'aparèixer
        # a cada bloc, a demés, deixa de ser necessària aquesta diferenciació,
        # ja que no hi una pestanya de menors sinó que els menors van a un
        # excel a banda
        #
        # Per tant, ara totes les activitats es llisten en aquest bloc.
        obj = self.get_sessions_obj()
        self.number_of_activities = len(obj)
        for item in obj:
            self.export_manager.row_number += 1

            project_sector = (
                item.get_project_sector_display() if item.project_sector else ""
            )
            types = item.get_types_display() if item.types else ""
            service = item.get_service_display() if item.service else ""
            sub_service = item.get_sub_service_display() if item.sub_service else ""
            communality_role = (
                item.get_communality_role_display() if item.communality_role else ""
            )
            networking = item.get_networking_display() if item.networking else ""
            town = ("", True)
            if item.place is not None and item.place.town:
                town = str(item.place.town)
            material_difusio = "No"
            if item.file1.name:
                material_difusio = "Sí"
            document_acreditatiu = "No"
            if item.photo2.name:
                document_acreditatiu = "Sí"

            row = [
                item.included_project,  # Projecte al qual s'engloba
                project_sector,  # Sector del projecte
                item.name,
                item.description,  # Descripció actuació
                types,  # Tipus actuació
                service,
                sub_service,
                communality_role,  # Rol Comunalitat
                networking,  # Treball en Xarxa
                item.agents_involved,  # Agents implicats
                item.date_start,
                "",  # Període d'actuacions
                town,
                item.neighborhood,  # Barri
                item.estimated_hours,  # Estimació hores dedicació
                material_difusio,  # Material de difusió
                "",  # Incidències
                document_acreditatiu,  # Document acreditatiu
                item.entities_str,  # Entitat
                str(item.place) if item.place else "",  # Lloc
                str(item.course),  # Acció
            ]
            self.export_manager.fill_row_data(row)

    def get_stages_obj(self):
        return ProjectStage.objects.order_by("date_start").filter(
            subsidy_period=self.export_manager.subsidy_period
        )

    def actuacions_rows_stages(self):
        """
        Acompanyaments que han d'aparèixer:
        - Tots els que siguin tipus Creació o Consolidació.
        - Idem però pels acompanyaments d'Incubació.
        Per tant com a màxim apareixerà 2 vegades.

        A banda hi ha l'exportació en 2 itineraris, on s'hi separaran els de
        Creació i els de Consolidació.
        """
        obj = self.get_stages_obj()
        self.stages_obj = {}
        for item in obj:
            if int(item.stage_type) not in self.stages_groups:
                continue
            group = self.stages_groups[int(item.stage_type)]
            p_id = item.project.id
            if p_id not in self.stages_obj:
                self.stages_obj.update({p_id: {}})
            if group not in self.stages_obj[p_id]:
                self.stages_obj[p_id].update(
                    {group: {"obj": item, "total_hours": 0, "participants": []}}
                )
            self.stages_obj[p_id][group]["total_hours"] += item.hours_sum()

            # Aprofitem per omplir les dades dels participants aquí per no
            # repetir el procés més endavant. La qüestió és que encara que un
            # participant hagi participat a diversos acompanyaments, aquí
            # només aparegui una vegada.
            for participant in item.partners_involved_in_sessions:
                if participant not in self.stages_obj[p_id][group]["participants"]:
                    self.stages_obj[p_id][group]["participants"].append(participant)
        """
        En aquest punt, self.stages_obj té aquesta estructura:
        160: {
            'nova_creacio': {
                'obj': '<ProjectStage: Consell Comarcal Conca de Barberà - Concactiva: 00 Nova creació - acollida>',
                'total_hours': 3,
                'participants': [
                         '<User: Jordi París>', '<User: Francesc Viñas>',
                         '<User: Carme Pallàs>',
                         '<User: Pere Picornell Busquets>'
                ],
                'row_number': 122
            }
        },
        20: {
            'consolidacio': {
                'obj': '<ProjectStage: La Providència SCCL: 04 Consolidació - acompanyament>',
                'total_hours': 36,
                'participants': [
                    '<User: Teresa Trilla Ferré>',
                    '<User: Marc Trilla Güell>',
                    '<User: Gerard Nogués Balsells>',
                    '<User: tais bastida aubareda>'
                ],
                'row_number': 126},
            'nova_creacio': {
                'obj': '<ProjectStage: La Providència SCCL: 02 Nova creació - constitució>',
                'total_hours': 7,
                'participants': [
                    '<User: Marc Trilla Güell>',
                    '<User: Esther Perello Piulats>'
                ],
                'row_number': 127
            }
        }, 
        
        És a dir, cada Projecte té un element amb la seva ID, que conté els
        grups que corresponguin.
        Cada grup conté:
            - Una instància de l'objecte ProjectStage (el primer que hagi pillat)
            - 'total_hours', amb la suma de totes les hores de tots els ProjectStages
                del mateix grup i projecte.

        A continuació el que farem és afegir com a row cada un d'aquests grups.
        De manera que cada itinerari (creació, consolidació..) de cada projecte
        tindrà la seva propia fila a Actuacions.
        
        En el procés de fer-ho, aprofitem per desar el nº de row dins 
        self.stages_obj[id_projecte][nom_grup][row_number]
        per poder-ho fer servir més endavant quan generem els rows de les 
        persones participants.
        """

        self.number_of_stages = 0
        for project_id, project in self.stages_obj.items():
            for group_name, group in project.items():
                self.number_of_stages += 1
                item = group["obj"]
                self.export_manager.row_number += 1

                # Desant el nº per quan fem el llistat de participants. El
                # self.export_manager.row_number conté el row REAL, que com que inclou la fila
                # de headers, és un més que la que s'assignarà com a
                # referència.
                self.stages_obj[project_id][group_name]["row_number"] = (
                    self.export_manager.row_number - 1
                )

                project_sector = item.get_project_sector_display() if item.project_sector else ""
                types = item.get_types_display() if item.types else ""
                service = item.get_service_display() if item.service else ""
                sub_service = item.get_sub_service_display() if item.sub_service else ""
                communality_role = (
                    item.get_communality_role_display() if item.communality_role else ""
                )
                networking = item.get_networking_display() if item.networking else ""
                town = ("", True)
                if item.project.town:
                    town = str(item.project.town)
                neighborhood = ("", True)
                if item.project.neighborhood:
                    neighborhood = str(item.project.neighborhood)
                hours_sum = ("", True)
                if item.hours_sum():
                    hours_sum = str(item.hours_sum())
        
                row = [
                    "",  # Projecte al qual s'engloba
                    project_sector,  # Sector del projecte
                    item.project.name,  # Nom de l'actuació
                    item.project.description,  # Descripció actuació
                    types,  # Tipus actuació
                    service,  # Servei
                    sub_service,  # Actuacions
                    communality_role,  # Rol communalitat
                    networking,  # Treball en Xarxa
                    item.agents_involved,  # Agents implicats
                    item.date_start or "",  # Data inici d'actuació
                    "",  # Període d'actuacions
                    town,
                    neighborhood,  # Barri
                    hours_sum,  # Estimació hores dedicació
                    "No",  # Material de difusió
                    "",  # Incidències
                    "",  # Document acreditatiu
                    "",  # Entitat
                    "(no aplicable)",  # Lloc
                    "(no aplicable)",  # Acció
                ]
                self.export_manager.fill_row_data(row)

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
                str(item.place) if item.place else "",  # Lloc
                str(item.course),  # Acció
            ]
            self.export_manager.fill_row_data(row)

    def actuacions_rows_founded_projects(self):
        """
        Tots els projectes que tinguin data de constitució dins de
        les dates de la convocatòria apareixeran
        a la pestanya d'EntitatsCreades.
        No obstant només aquells que tinguin una actuació vinculada
        durant el període de la convocatòria han de
        d'aparèixer a la pestanya d'Actuacions.

        Els que tenen això vol dir que hi ha hagut un acompanyament
        del projecte dins de la convocatòria.
        Poden haver-hi hagut varis acompanyaments, per tant, hem
        de d'obtenir l'acompanyament més recent.

        Si tot això existeix mostrem les dades del més recent,
         sinó, ignorem el projecte.

        Després a la pestanya d'EntitatsCreades hem de fer el
        mateix filtre per saber quins tenen
        actuació creada, i deduïr per l'ordre quina ID li toca.
        """
        obj = Project.objects.filter(
            constitution_date__range=self.export_manager.subsidy_period_range
        )
        self.number_of_founded_projects = len(obj)
        for project in obj:
            stages = ProjectStage.objects.filter(
                project=project, subsidy_period=self.export_manager.subsidy_period
            ).order_by("-date_start")[:1]
            if stages.count() < 1:
                continue
            stage = stages.all()[0]

            self.export_manager.row_number += 1
            service = stage.get_service_display() if stage.service else ""
            sub_service = stage.get_sub_service_display() if stage.sub_service else ""
            town = ("", True)
            if project.town:
                town = str(project.town)

            row = [
                "", # Projecte al qual s'engloba
                "", # Sector del projecte
                project.name,
                "", # Descripció actuació
                "", # Tipus actuació
                service,
                sub_service,
                "", # Rol Comunalitat
                "", # Treball en Xarxa
                "", # Agents implicats
                stage.date_start,
                "",  # Període
                town,
                "",  # Barri
                "",  # Estimació hores dedicació
                "No",  # Material de difusió
                "",  # Incidències
                "",  # Doc. acreditatiu
                "",  # Entitat
                "(no aplicable)",  # Lloc
                "(no aplicable)",  # Acció
            ]
            self.export_manager.fill_row_data(row)

    def export_stages(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Acompanyaments"
        )
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 20),
            ("Nom actuació", 40),
            ("Nom de projecte/empresa o entitat", 35),
            ("Destinatari de l'acompanyament", 30),
            ("Tipus d'acompanyament: creació/consolidació/creixement", 30),
            ("Data d'inici", 13),
            ("Barri", 20),
            ("Municipi", 20),
            ("Breu descripció de l'actuació", 50),
            ("Total hores d'acompanyament", 10),
            ("[Data última sessió]", 10),
        ]
        self.export_manager.create_columns(columns)

        self.stages_rows()

    def stages_rows(self):
        reference_number = self.number_of_activities

        for p_id, stage in self.stages_obj.items():
            for group_name, group in stage.items():
                self.export_manager.row_number += 1
                reference_number += 1
                item = group["obj"]
                stage_type = self.export_manager.get_correlation(
                    "stage_type",
                    item.stage_type,
                )
                # hours = item.hours if item.hours is not None else ("", True)
                hours = group["total_hours"]
                town = ("", True)
                if item.project.town:
                    town = str(item.project.town)

                row = [
                    self.get_formatted_reference(
                        reference_number,
                        item.service,
                        item.project.name,
                    ),  # Referència.
                    "",  # Nom actuació. Camp no editable.
                    item.project.name,
                    stage_type,  # Tipus d'acompanyament
                    item.date_start or ("", True),
                    item.project.neighborhood or ("", True),
                    town,
                    item.project.description,  # Breu descripció.
                    hours,  # Total d'hores d'acompanyament.
                    item.latest_session.date if item.latest_session else "",
                ]
                self.export_manager.fill_row_data(row)

    def export_founded_projects(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Creació d'entitats"
        )
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 10),
            ("Projecte al qual s'engloba", 40),
            ("Sector de l'activitat", 40),
            ("Nom d'actuació", 40),
            ("Nom entitat", 40),
            ("NIF entitat", 40),
            ("Tipus d'entitat", 40),
            ("Sector activitat", 40),
            ("Nom i cognoms persona de contacte", 30),
            ("Municipi", 30),
            ("Barri", 30),
            ("Correu electrònic", 12),
            ("Telèfon", 10),
            ("Anualitat", 20),
            ("Economia solidària (revisar)", 35),
            ("[Acompanyaments]", 10),
        ]
        self.export_manager.create_columns(columns)

        self.founded_projects_rows()

    def founded_projects_rows(self):
        # The Ids start at 1, so later we add 1 to this number to have the
        # right ID.
        founded_projects_reference_number = (
            self.number_of_stages
            + self.number_of_activities
            + self.number_of_nouniversitaris
        )
        obj = Project.objects.filter(
            constitution_date__range=self.export_manager.subsidy_period_range
        )
        for project in obj:
            # Repeating the same filter than in Actuacions to determine if we
            # have an Actuació or not
            reference_number = ""
            name = ""
            stages = ProjectStage.objects.filter(
                project=project, subsidy_period=self.export_manager.subsidy_period
            ).order_by("-date_start")[:1]
            if stages.count() > 0:
                stage = stages.all()[0]
                founded_projects_reference_number += 1
                reference_number = self.get_formatted_reference(
                    founded_projects_reference_number,
                    stage.service,
                    project.name,
                )
                name = project.name
            project_sector = project.get_project_sector_display() if project.project_sector else ""
            annuity = project.get_annuity_display() if project.annuity else ""
            entity_type = project.get_entity_type_display() if project.entity_type else ""

            self.export_manager.row_number += 1
            row = [
                reference_number,
                # Referència. En aquest full no cal que tinguin relació amb Actuacions.
                "", # Projecte al qual s'engloba
                "", # Sector de l'activitaxt
                name, # Nom de l'actuació. En aquest full no cal que tinguin relació amb Actuacions.
                project.entity_name, # Nom entitat
                project.cif, # NIF entitat
                entity_type, # Tipus d'entitat
                project_sector, # Sector activitat
                project.partners.all()[0].full_name if project.partners.all() else "",
                str(project.town), 
                project.neighborhood,
                project.mail,
                project.phone,
                annuity, # Anualitat
                "Sí",  # Economia solidària
                project.stages_list,
            ]
            self.export_manager.fill_row_data(row)

    def export_participants(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Persones Participants o Ateses",
        )
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 40),
            ("Nom d'actuació", 40),
            ("Projecte al qual s'engloba", 40),
            ("Sector de l'activitat", 40),
            ("Cognoms", 20),
            ("Nom", 10),
            ("Gènere", 10),
            ("Data naixement", 10),
            ("[Situació laboral]", 20),
            ("[Nivell d'estudis]", 20),
            ("[Com ens has conegut]", 20),
            ("[Email]", 30),
            ("[Telèfon]", 30),
            ("[Projecte]", 30),
        ]
        self.export_manager.create_columns(columns)

        self.participants_rows()
        self.participants_project_stages_rows()

    def participants_project_stages_rows(self):
        for project_id, project in self.stages_obj.items():
            for group_name, group in project.items():
                activity = group["obj"]
                activity_reference_number = group["row_number"]
                for participant in group["participants"]:
                    gender = ("", True)
                    if participant.gender:
                        gender = self.export_manager.get_correlation(
                            "gender",
                            participant.gender,
                        )

                    row = [
                        self.get_formatted_reference(
                            activity_reference_number,
                            activity.service,
                            activity.project.name,
                        ),
                        "",  # Nom de l'actuació. Camp automàtic de l'excel.
                        "",  # Projecte al qual s'engloba. Camp automàtic de l'excel.
                        "",  # Sector de l'activitat. Camp automàtic de l'excel.
                        participant.surname or "",
                        participant.first_name,
                        participant.id_number or ("", True),
                        gender,
                        participant.birthdate or ("", True),
                        participant.get_employment_situation_display() or "",
                        participant.get_educational_level_display() or "",
                        participant.get_discovered_us_display() or "",
                        participant.email,
                        participant.phone_number or "",
                        str(participant.project) or "",
                    ]
                    self.export_manager.row_number += 1
                    self.export_manager.fill_row_data(row)

    def participants_rows(self):
        activity_reference_number = 0
        obj = self.get_sessions_obj()
        for activity in obj:
            # We know that activities where generated first, so it starts at 1.
            activity_reference_number += 1
            for enrollment in activity.confirmed_enrollments:
                participant = enrollment.user
                self.export_manager.row_number += 1
                gender = ("", True)
                if participant.gender:
                    gender = self.export_manager.get_correlation(
                        "gender",
                        participant.gender,
                    )

                row = [
                    self.get_formatted_reference(
                        activity_reference_number,
                        activity.service,
                        activity.name,
                    ),
                    "",  # Nom de l'actuació. Camp automàtic de l'excel.
                    participant.surname or "",
                    participant.first_name,
                    participant.id_number or ("", True),
                    gender,
                    participant.birthdate or ("", True),
                    participant.get_employment_situation_display() or "",
                    participant.get_educational_level_display() or "",
                    participant.get_discovered_us_display() or "",
                    participant.email,
                    participant.phone_number or "",
                    str(participant.project) if participant.project else "",
                ]
                self.export_manager.fill_row_data(row)

    def export_nouniversitaris(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
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
        nouniversitari_reference_number = (
            self.number_of_stages + self.number_of_activities
        )
        obj = self.get_sessions_obj()
        for activity in obj:
            self.export_manager.row_number += 1
            nouniversitari_reference_number += 1
            row = [
                self.get_formatted_reference(
                    nouniversitari_reference_number,
                    activity.service,
                    activity.project.name,
                ),
                # Referència.
                activity.name,  # Nom de l'actuació. Camp automàtic de l'excel.
                self.export_manager.get_correlation(
                    "minors_grade", activity.minors_grade
                ),
                activity.minors_school_name,
            ]
            self.export_manager.fill_row_data(row)

    def export_insercionslaborals(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Persones Inserides"
        )
        self.export_manager.row_number = 1

        columns = [
            ("Referència (omplir a ma)", 20),
            ("Projecte al qual s'engloba", 20),
            ("Sector de l'activitat", 20),
            ("Nom actuació", 20),
            ("DNI o NIE persona inserida", 20),
            ("Cognoms", 20),
            ("Nom", 20),
            ("Gènere", 20),
            ("Data naixement", 20),
            ("NIF Entitat", 20),
            ("Nom entitat on s'insereix", 20),
            ("Sector de l'entitat", 20),
            ("Tipus contracte o vinculació", 20),
            ("Data alta SS", 20),
            ("Data baixa SS", 20),
            ("Municipi Entitat", 20),
            ("Barri Entitat", 20),
            ("[ convocatòria ]", 20),
        ]
        self.export_manager.create_columns(columns)

        self.insercionslaborals_rows()

    def insercionslaborals_rows(self):
        obj = EmploymentInsertion.objects.filter(
            subsidy_period__date_start__range=self.export_manager.subsidy_period_range
        )
        for insertion in obj:
            self.export_manager.row_number += 1
            id_number = insertion.user.id_number
            if not id_number:
                id_number = ("", True)
            insertion_date = insertion.insertion_date
            if not insertion_date:
                insertion_date = ("", True)
            end_date = insertion.end_date or ""
            contract_type = insertion.get_contract_type_display()
            if not contract_type:
                contract_type = ("", True)
            birthdate = insertion.user.birthdate
            if not birthdate:
                birthdate = ("", True)
            if insertion.user.gender is None:
                gender = ""
            else:
                gender = self.export_manager.get_correlation(
                    "gender", insertion.user.gender
                )
            entity_sector = insertion.get_entity_sector_display()

            row = [
                "",  # TODO: des d'aquí no podem saber la referència de l'Activitat
                "",  # Projecte al qual s'engloba
                "",  # Sector de l'activitat
                "",  # Nom actuació
                id_number,
                insertion.user.surname,
                insertion.user.first_name,
                gender,
                birthdate,
                insertion.entity_nif,
                insertion.entity_name,
                entity_sector,
                contract_type,
                insertion_date,  # Data d'alta SS
                end_date,  # Data baixa SS
                str(insertion.entity_town),
                insertion.entity_neighborhood,
                str(insertion.subsidy_period),  # Convocatòria
            ]
            self.export_manager.fill_row_data(row)

    def export_all_projects(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "PROJECTES"
        )
        self.export_manager.row_number = 1

        columns = [
            ("ID", 5),
            ("Data registre", 12),
            ("Nom de l'entitat", 40),
            ("Nom i cognoms persona de contacte", 30),
            ("Correu electrònic", 30),
            ("Telèfon", 15),
            ("[Acompanyaments]", 40),
            ("[Serveis]", 40),
        ]
        self.export_manager.create_columns(columns)

        self.all_projects_rows()

    def all_projects_rows(self):
        self.export_manager.row_number = 1
        obj = Project.objects.order_by("id").all()
        for project in obj:
            self.export_manager.row_number += 1
            row = [
                project.id,
                project.registration_date if project.registration_date else "",
                project.name,
                project.partners.all()[0].full_name if project.partners.all() else "",
                project.mail,
                project.phone,
                project.stages_list if project.stages_list else "",
                project.services_list if project.services_list else "",
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
        return f"{ref_num} {service_code}) {subsidy_period} {actuation_name}"
