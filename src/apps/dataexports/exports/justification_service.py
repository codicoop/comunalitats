from apps.cc_courses.models import Activity, ActivityEnrolled
from apps.dataexports.exports.manager import ExcelExportManager
from apps.projects.models import ProjectStage, Project, EmploymentInsertion


class ExportJustificationService:
    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.number_of_activities = 0
        self.number_of_stages = 0
        self.number_of_nouniversitaris = 0
        self.number_of_founded_projects = 0
        # La majoria d'ateneus volen que hi hagi una sola actuació per un
        # projecte encara que hagi tingut diferents tipus d'acompanyament.
        # CoopCamp (i potser algun altre?) volen separar-ho per itineraris,
        # de manera que hi hagi una actuació per l'itinerari de Nova Creació i
        # una pel de Consolidació.
        # Per defecte ho definim per 1 itinerari.
        self.stages_groups = {
            # 1: 'nova_creacio',
            # 2: 'nova_creacio',
            # 6: 'nova_creacio',
            # 7: 'nova_creacio',
            # 8: 'nova_creacio',
            9: 'creacio',  # Era Incubació
            11: 'creacio',  # Creació
            12: 'creacio',  # Consolidació
        }
        self.stages_obj = None

    def get_sessions_obj(self, for_minors=False):
        return Activity.objects.filter(
            date_start__range=self.export_manager.subsidy_period.range,
            for_minors=for_minors
        )
    
    """
    
    Exportació Ateneu
    
    """
    def export(self):
        """ Each function here called handles the creation of one of the
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
        self.actuacions_rows_activities()
        self.actuacions_rows_stages()
        self.actuacions_rows_nouniversitaris()
        self.actuacions_rows_founded_projects()
        # Total Stages: self.export_manager.row_number-Total Activities-1

    def actuacions_rows_activities(self):
        obj = self.get_sessions_obj()
        self.number_of_activities = len(obj)
        for item in obj:
            self.export_manager.row_number += 1

            service = item.get_service_display() if item.service else ""
            sub_service = item.get_sub_service_display() if item.sub_service else ""
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
                service,
                sub_service,
                item.name,
                item.date_start,
                "",  # Període
                town,
                material_difusio,
                "",
                document_acreditatiu,
                item.entities_str,  # Entitat
                str(item.place) if item.place else '',  # Lloc
                str(item.course),  # Acció
            ]
            self.export_manager.fill_row_data(row)

    def get_stages_obj(self):
        return ProjectStage.objects.order_by('date_start').filter(
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
                self.stages_obj.update({
                    p_id: {}
                })
            if group not in self.stages_obj[p_id]:
                self.stages_obj[p_id].update({
                    group: {
                        'obj': item,
                        'total_hours': 0,
                        'participants': []
                    }
                })
            self.stages_obj[p_id][group]['total_hours'] += item.hours_sum()

            # Aprofitem per omplir les dades dels participants aquí per no
            # repetir el procés més endavant. La qüestió és que encara que un
            # participant hagi participat a diversos acompanyaments, aquí
            # només aparegui una vegada.
            for participant in item.involved_partners.all():
                if (
                        participant
                        not in self.stages_obj[p_id][group]['participants']
                ):
                    self.stages_obj[p_id][group]['participants'].append(
                        participant
                    )
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
                item = group['obj']
                self.export_manager.row_number += 1

                # Desant el nº per quan fem el llistat de participants. El
                # self.export_manager.row_number conté el row REAL, que com que inclou la fila
                # de headers, és un més que la que s'assignarà com a
                # referència.
                self.stages_obj[project_id][group_name][
                    'row_number'
                ] = self.export_manager.row_number - 1

                service = item.get_service_display() if item.service else ""
                sub_service = item.get_sub_service_display() if item.sub_service else ""
                town = ("", True)
                if item.project.town:
                    town = str(item.project.town)

                row = [
                    service,
                    sub_service,
                    item.project.name,
                    item.date_start or '',
                    town,
                    "No",  # Material de difusió
                    "",  # Incidències
                    "",  # Document acreditatiu
                    # En blanc pq cada stage session pot contenir una entitat
                    "",  # Entitat
                    '(no aplicable)',  # Lloc
                    '(no aplicable)',  # Acció
                ]
                self.export_manager.fill_row_data(row)

    def actuacions_rows_nouniversitaris(self):
        obj = self.get_sessions_obj(for_minors=True)
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
                item.entities_str,  # Entitat
                document_acreditatiu,
                "",
                str(item.entity) if item.entity else '',  # Entitat
                str(item.place) if item.place else '',  # Lloc
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
            constitution_date__range=self.export_manager.subsidy_period_range)
        self.number_of_founded_projects = len(obj)
        for project in obj:
            stages = ProjectStage.objects.filter(
                project=project,
                subsidy_period=self.export_manager.subsidy_period
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
                service,
                sub_service,
                project.name,
                stage.date_start,
                "",  # Període
                town,
                "No",  # Material de difusió
                "",  # Incidències
                # En blanc pq cada stage session pot contenir una entitat
                "",  # Entitat
                '(no aplicable)',  # Lloc
                '(no aplicable)',  # Acció
            ]
            self.export_manager.fill_row_data(row)

    def export_stages(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Acompanyaments")
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 20),
            ("Nom actuació", 40),
            ("Destinatari de l'acompanyament (revisar)", 45),
            ("En cas d'entitat (nom de l'entitat)", 40),
            ("En cas d'entitat (revisar)", 30),
            ("Creació/consolidació", 18),
            ("Data d'inici", 13),
            ("Localitat", 20),
            ("Breu descripció del projecte", 50),
            ("Total hores d'acompanyament", 10),
            ("[Data fi]", 13),
        ]
        self.export_manager.create_columns(columns)

        self.stages_rows()

    def stages_rows(self):
        reference_number = self.number_of_activities

        for p_id, stage in self.stages_obj.items():
            for group_name, group in stage.items():
                self.export_manager.row_number += 1
                reference_number += 1
                item = group['obj']

                # hours = item.hours if item.hours is not None else ("", True)
                hours = group['total_hours']
                town = ("", True)
                if item.project.town:
                    town = str(item.project.town)
                crea_consolida = item.get_stage_type_display()

                row = [
                    f"{reference_number} {item.project.name}",  # Referència.
                    item.project.name,
                    # Camp no editable, l'ha d'omplir l'excel automàticament.
                    "Entitat",
                    # "Destinatari de l'actuació" Opcions: Persona física/Promotor del projecte/Entitat PENDENT.
                    item.project.name,  # "En cas d'entitat (Nom de l'entitat)"
                    self.export_manager.get_correlation(
                        "project_status", item.project.project_status),
                    crea_consolida if crea_consolida else '',
                    # "Creació/consolidació".
                    item.date_start if item.date_start else '',
                    town,
                    item.project.description,  # Breu descripció.
                    hours,  # Total hores d'acompanyament.
                    item.latest_session.date if item.latest_session else '',
                ]
                self.export_manager.fill_row_data(row)

    def export_founded_projects(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet("Creació d'entitats")
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 10),
            ("Nom actuació", 40),
            ("Nom de l'entitat", 40),
            ("NIF de l'entitat", 12),
            ("Nom i cognoms persona de contacte", 30),
            ("Correu electrònic", 12),
            ("Telèfon", 10),
            ("Economia solidària (revisar)", 35),
            ("[Acompanyaments]", 10),
        ]
        self.export_manager.create_columns(columns)

        self.founded_projects_rows()

    def founded_projects_rows(self):
        # The Ids start at 1, so later we add 1 to this number to have the 
        # right ID.
        founded_projects_reference_number = \
            self.number_of_stages \
            + self.number_of_activities \
            + self.number_of_nouniversitaris
        obj = Project.objects.filter(
            constitution_date__range=self.export_manager.subsidy_period_range)
        for project in obj:
            # Repeating the same filter than in Actuacions to determine if we 
            # have an Actuació or not
            reference_number = ""
            name = ""
            stages = ProjectStage.objects.filter(
                project=project,
                subsidy_period=self.export_manager.subsidy_period
            ).order_by("-date_start")[:1]
            if stages.count() > 0:
                stage = stages.all()[0]
                founded_projects_reference_number += 1
                reference_number = (f"{founded_projects_reference_number} "
                                    f"{project.name}")
                name = project.name

            self.export_manager.row_number += 1
            if project.cif is None:
                self.export_manager.error_message.add(
                    "<p><strong>Error: falta NIF</strong>. L'entitat '{}' "
                    "apareix com a EntitatCreada"
                    " perquè té una Data de constitució dins de "
                    "la convocatòria, però si no té NIF, "
                    "no pot ser inclosa a l'excel.</p>".format(project.name))
                project.cif = ""
            row = [
                reference_number,
                # Referència. En aquest full no cal que tinguin relació amb Actuacions.
                name,
                # Nom de l'actuació. En aquest full no cal que tinguin relació amb Actuacions.
                project.name,
                project.cif,
                project.partners.all()[
                    0].full_name if project.partners.all() else "",
                project.mail,
                project.phone,
                "Sí",  # Economia solidària
                project.stages_list
            ]
            self.export_manager.fill_row_data(row)

    def export_participants(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet(
                "Persones Participants o Ateses",
            )
        self.export_manager.row_number = 1

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
            ("[Nivell d'estudis]", 20),
            ("[Com ens has conegut]", 20),
            ("[Email]", 30),
            ("[Telèfon]", 30),
            ("[Projecte]", 30),
            ("[Acompanyaments]", 30),
        ]
        self.export_manager.create_columns(columns)

        self.participants_rows()
        self.participants_project_stages_rows()

    def participants_project_stages_rows(self):
        for project_id, project in self.stages_obj.items():
            for group_name, group in project.items():
                activity = group['obj']
                activity_reference_number = group['row_number']
                for participant in group['participants']:
                    if participant.gender is None:
                        gender = ""
                    else:
                        gender = self.export_manager.get_correlation(
                            'gender', participant.gender)
                    town = ""
                    if participant.town:
                        town = participant.town.name

                    row = [
                        f"{activity_reference_number} {activity.project.name}",
                        # Referència.
                        activity.project.name,
                        # Nom de l'actuació. Camp automàtic de l'excel.
                        participant.surname or "",
                        participant.first_name,
                        participant.id_number,
                        gender if gender else "",
                        participant.birthdate or "",
                        town,
                        participant.get_employment_situation_display() or "",
                        participant.get_educational_level_display() or "",
                        participant.get_discovered_us_display() or "",
                        participant.email,
                        participant.phone_number or "",
                        str(participant.project) or "",
                        participant.project.stages_list if participant.project and participant.project.stages_list else "",
                    ]
                    self.export_manager.row_number += 1
                    self.export_manager.fill_row_data(row)

    def participants_rows(self):
        activity_reference_number = 0
        obj = self.get_sessions_obj(for_minors=False)
        for activity in obj:
            # We know that activities where generated first, so it starts at 1.
            activity_reference_number += 1
            for enrollment in activity.confirmed_enrollments:
                participant = enrollment.user
                self.export_manager.row_number += 1
                if participant.gender is None:
                    gender = ""
                else:
                    gender = self.export_manager.get_correlation(
                        'gender', participant.gender)
                town = ""
                if participant.town:
                    town = participant.town.name

                row = [
                    f"{activity_reference_number} {activity.name}",
                    # Referència.
                    activity.name,
                    # Nom de l'actuació. Camp automàtic de l'excel.
                    participant.surname if participant.surname else "",
                    participant.first_name,
                    participant.id_number,
                    gender if gender else "",
                    participant.birthdate if participant.birthdate else "",
                    town,
                    participant.get_employment_situation_display() or "",
                    participant.get_educational_level_display() or "",
                    participant.get_discovered_us_display() or "",
                    participant.email,
                    participant.phone_number or "",
                    str(participant.project) if participant.project else "",
                    participant.project.stages_list if participant.project and participant.project.stages_list else "",
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
        nouniversitari_reference_number = \
            self.number_of_stages \
            + self.number_of_activities
        obj = self.get_sessions_obj(for_minors=True)
        for activity in obj:
            self.export_manager.row_number += 1
            nouniversitari_reference_number += 1
            row = [
                f"{nouniversitari_reference_number} {activity.name}",
                # Referència.
                activity.name,  # Nom de l'actuació. Camp automàtic de l'excel.
                self.export_manager.get_correlation(
                    'minors_grade', activity.minors_grade),
                activity.minors_school_name,
            ]
            self.export_manager.fill_row_data(row)

    def export_insercionslaborals(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet("Persones Inserides")
        self.export_manager.row_number = 1

        columns = [
            ("Referència (omplir a ma)", 20),
            ("Nom actuació", 20),
            ("Cognoms", 20),
            ("Nom", 20),
            ("DNI o NIE persona inserida", 20),
            ("Data alta SS", 20),
            ("Data baixa SS", 20),
            ("Tipus contracte o vinculació", 20),
            ("Gènere", 20),
            ("Data naixement", 20),
            ("Nom entitat on s'insereix", 20),
            ("NIF Entitat", 20),
            ("Municipi Entitat", 20),
            ("Barri Entitat", 20),
            ("[ convocatòria ]", 20),
        ]
        self.export_manager.create_columns(columns)

        self.insercionslaborals_rows()

    def insercionslaborals_rows(self):
        obj = EmploymentInsertion.objects.filter(
            subsidy_period__date_start__range=self.export_manager.subsidy_period_range)
        for insertion in obj:
            self.export_manager.row_number += 1
            id_number = insertion.user.id_number
            if not id_number:
                id_number = ('', True)
            insertion_date = insertion.insertion_date
            if not insertion_date:
                insertion_date = ('', True)
            end_date = insertion.end_date
            if not end_date:
                end_date = ('', True)
            contract_type = insertion.get_contract_type_display()
            if not contract_type:
                contract_type = ('', True)
            birthdate = insertion.user.birthdate
            if not birthdate:
                birthdate = ('', True)

            if insertion.user.gender is None:
                gender = ""
            else:
                gender = self.export_manager.get_correlation(
                    'gender', insertion.user.gender)

            row = [
                '',  # Deixem referència en blanc pq la posin a ma.
                '',  # Nom actuació
                insertion.user.surname,
                insertion.user.first_name,
                id_number,
                insertion_date,  # Data d'alta SS
                end_date,  # Data baixa SS
                contract_type,
                gender,
                birthdate,
                insertion.entity_name,
                insertion.entity_nif,
                str(insertion.entity_town),
                insertion.entity_neighborhood,
                str(insertion.subsidy_period),  # Convocatòria
            ]
            self.export_manager.fill_row_data(row)

    def export_all_projects(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet("PROJECTES")
        self.export_manager.row_number = 1

        columns = [
            ("ID", 5),
            ("Data registre", 12),
            ("Data constitució", 12),
            ("Nom de l'entitat", 40),
            ("NIF de l'entitat", 12),
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
        obj = Project.objects.order_by('id').all()
        for project in obj:
            self.export_manager.row_number += 1
            row = [
                project.id,
                project.registration_date if project.registration_date else "",
                project.constitution_date if project.constitution_date else "",
                project.name,
                project.cif if project.cif else "",
                project.partners.all()[
                    0].full_name if project.partners.all() else "",
                project.mail,
                project.phone,
                project.stages_list if project.stages_list else "",
                project.services_list if project.services_list else ""
            ]
            self.export_manager.fill_row_data(row)
