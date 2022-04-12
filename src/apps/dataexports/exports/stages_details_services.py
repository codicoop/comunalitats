import numbers

from django.db.models import Sum, Q, Count
from openpyxl.styles.numbers import FORMAT_PERCENTAGE

from apps.coopolis.choices import CirclesChoices, ServicesChoices
from apps.coopolis.models import ProjectStage
from apps.coopolis.models.projects import ProjectStageSession, StageSubtype
from apps.dataexports.exports.manager import ExcelExportManager


class ExportStagesDetailsServices:
    """
    Descripció del procés de generació de l'exportació

    Aquesta classe fa d'intermediaria entre diversos managers.
    - ExcelExportManager que s'encarrega de generar el format excel.
    Els altres 3, tots ells extenen StageDetailsDataManager, però 
    StageDetailsDataManager únicament declara self.subsidy_period i el mètode
    none_as_zero():
    - CirclesDataManager
    - CirclesPerUserDataManager
    - StageTypesDataManager
    
    El punt d'entrada és ExportStagesDetailsServices.export(), que crida 
        self.export_circles() <- genera un dels fulls de l'excel
        self.export_stage() <- genera un dels fulls de l'excel
    i finalment retorna el propi fitxer per ser descarregat.

    Quan s'executa self.export(), totes les dades ja s'han omplert durant el
    self.__init__().

    PROCÉS DE GENERAR DADES DEL PRIMER FULL DURANT LA INICIALITZACIÓ
        PART A: DADES PER CADA UN DELS CERCLES

    ## self.circles_data
    self.circles_data s'omple fent servir CirclesDataManager.get_circles_data()

    ### CirclesDataManager.get_circles_data()

    Es genera un queryset per cada un dels cercles, omplint els camps:
    f'hours_{circle.name}_certified'
    f'hours_{circle.name}_uncertified'
    ... per cada un.

    Aquest queryset s'executa contra ProjectStage agrupant per 'service',
    és a dir, que per cada Servei QUE CONTINGUI DADES es retorna el conjunt de
    dades de cada cercle.
    Important tenir en compte que els serveis que no tenen dades directament no
    existiran en els sets de dades que es faran servir més endavant per omplir
    els templates:

    <QuerySet [
        {
            'service': 10,
            'hours_CERCLE0_certified': None,
            'hours_CERCLE0_uncertified': None,
            'hours_CERCLE1_certified': None,
            'hours_CERCLE1_uncertified': None,
            'hours_CERCLE2_certified': None,
            'hours_CERCLE2_uncertified': None,
            'hours_CERCLE3_certified': None,
            'hours_CERCLE3_uncertified': 1.5,
            'hours_CERCLE4_certified': None,
            'hours_CERCLE4_uncertified': None,
            'hours_CERCLE5_certified': None,
            'hours_CERCLE5_uncertified': None
        }, {
            'service': None,
            'hours_CERCLE0_certified': 90.0,
            'hours_CERCLE0_uncertified': 105.0,
            'hours_CERCLE1_certified': None,
            'hours_CERCLE1_uncertified': None,
            'hours_CERCLE2_certified': None,
            'hours_CERCLE2_uncertified': None,
            'hours_CERCLE3_certified': None,
            'hours_CERCLE3_uncertified': None,
            'hours_CERCLE4_certified': 80.0,
            'hours_CERCLE4_uncertified': 10.0,
            'hours_CERCLE5_certified': None,
            'hours_CERCLE5_uncertified': None
        }, {
            'service': 40,
            'hours_CERCLE0_certified': 4.0,
            'hours_CERCLE0_uncertified': 20.0,
            'hours_CERCLE1_certified': None,
            'hours_CERCLE1_uncertified': 2.0,
            'hours_CERCLE2_certified': None,
            'hours_CERCLE2_uncertified': None,
            'hours_CERCLE3_certified': None,
            'hours_CERCLE3_uncertified': None,
            'hours_CERCLE4_certified': None,
            'hours_CERCLE4_uncertified': 8.0,
            'hours_CERCLE5_certified': None,
            'hours_CERCLE5_uncertified': None
        }
    ]>

    Aquestes dades on cop consultades a ProjectStage es passen pel mètode
    ExportStagesDetailsServices.format_circles_data()

    ## ExportStagesDetailsServices.format_circles_data()

    Aquí s'obté tot l'esquelet de les dades (que anomenem template) amb
    template = self.get_data_structure()
    I després fa un bucle en el que va col·locant cada una de les dades al
    lloc corresponent del template.
    Aquest template ara té l'estructura i les dades que més endavant s'agafaran
    per transformat en columnes i rows de l'excel.

    PROCÉS DE GENERAR DADES DEL PRIMER FULL DURANT LA INICIALITZACIÓ
        PART B: DADES PER CADA UNA DE LES PERSONES DE L'EQUIP

    ## self.users_data = CirclesPerUserDataManager(...).get_data()

    A través d'aquest mètode s'acaba omplint les dades que més endavant durant
    l'export, quan arribi a self.circles_ateneu_user_rows(), s'afegiran com a
    blocs de rows per cada un dels users, agrupats per cercles.

    self.users_data:
    {'CERCLE0': {'values': [['(sense usuari)', 0, 0, 1.0],
                            ['Nom Usuari A', 6, 36.0, 10.0],
                            ['Nom Usuari B', 3, 0, 0],
                            ['etc...', 2, 0, 6.0],
                 'verbose_name': 'Ateneu'},
     'CERCLE1': {'values': [['(sense usuari)', 0, 0, 1.0],
                            ['Nom Usuari A', 6, 0, 10.0],
                            ['Nom Usuari B', 3, 0, 0],
                            ['etc...', 2, 0, 6.0],
                 'verbose_name': 'Consum i Transició Agroecològica'},
     'CERCLE2': {...

    GENERACIÓ DEL PRIMER FULL (Ateneu-Cercles)

    Es crida circle_n_rows() per cada un dels cercles possibles.
    Cada fila que això generarà té 4 columnes:
        Nom, Bases convo, Justicades, Sense justificar.

    I agafa les dades que s'han omplert durant la inicialització de la class,
    que son a self.circles_data.
    Ho fa així: rows = self.circles_data[circle.name].values()
    Dins de self.circle_n_rows(circle)

    PROCÉS DE GENERAR LES DADES PEL 2N FULL DURANT LA INICIALITZACIÓ

    S'omplen dues propietats:
        self.stage_types_data["totals"],
        self.stage_types_data["users"]

    ## self.stage_types_data["totals"]:
    [{'totals': ['Creació - (cap)', 0, 0, 0, 0], 'users': []},
     {'totals': ['Creació - Acollida', 88.5, 54.0, 34.5, 0], 'users': []},
     {'totals': ['Creació - Constitució', 63.5, 24.0, 39.5, 0], 'users': []},
     {'totals': ['Creació - Acompanyament', 0, 0, 0, 0], 'users': []},
     {'totals': ['Creació - Procés', 125.0, 70.0, 55.0, 0], 'users': []},
     {'totals': ['Consolidació - (cap)', 0, 0, 0, 0], 'users': []},
     {'totals': ['Consolidació - Acollida', 88.5, 54.0, 34.5, 0], 'users': []},
     {'totals': ['Consolidació - Constitució', 63.5, 24.0, 39.5, 0], 'users': []},
     {'totals': ['Consolidació - Acompanyament', 0, 0, 0, 0], 'users': []},
     {'totals': ['Consolidació - Procés', 125.0, 70.0, 55.0, 0], 'users': []}]


    ## self.stage_types_data["users"]:
    {11: {'name': 'creation',
          'subtypes': {0: {'users': [], 'verbose_name': 'Sense subtipus'},
                       1: {'users': [['Nom Usuari 1', 1, 0, 3.0, 0],
                                     ['Nom Usuari 2', 17, 14.0, 19.5, 0],
                                     ['Nom Usuari ETC', 6, 10.0, 5.0, 0],
                           'verbose_name': 'Acollida'},
                       2: {'users': [['Nom Usuari 1', 4, 0, 17.0, 0],
                                     ['Nom Usuari 2', 2, 0, 5.0, 0],
                                     ['Nom Usuari ETC', 25, 20.0, 30.0, 0],
                           'verbose_name': 'Procés'},
                       3: {'users': [['Nom Usuari 1', 1, 10.0, 0, 0],
                                     ['Nom Usuari 2', 1, 0, 1.0, 0],
                                     ['Nom Usuari ETC', 26, 14.0, 27.5, 0],
                           'verbose_name': 'Constitució'},
                       4: {'users': [], 'verbose_name': 'Acompanyament'}},
          'verbose_name': 'Creació'},
     12: {'name': 'consolidation',
          'subtypes': {0: {'users': [], 'verbose_name': 'Sense subtipus'},
                       1: {'users': [['Nom Usuari 1', 1, 0, 2.0, 0],
                                     ['Nom Usuari 2', 1, 0, 2.0, 0],
                                     ['Nom Usuari ETC', 1, 0, 4.0, 0],
                           'verbose_name': 'Acollida'},
                       2: {'users': [], 'verbose_name': 'Procés'},
                       3: {'users': [], 'verbose_name': 'Constitució'},
                       4: {'users': [['Nom Usuari 1', 1, 0, 0, 0],
                                     ['Nom Usuari 2', 2, 0, 3.5, 0],
                                     ['Nom Usuari ETC', 1, 0, 0, 0],
                           'verbose_name': 'Acompanyament'}},
          'verbose_name': 'Consolidació'}}

    Mitjançant el mètode:
    StageTypesDataManager(...).get_data()

    """
    circles_data = None
    users_data = None
    stage_types_data = {}

    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.circles_data = CirclesDataManager(
            self.export_manager.subsidy_period
        ).get_circles_data()
        self.users_data = CirclesPerUserDataManager(
            self.export_manager.subsidy_period
        ).get_data()
        (
            self.stage_types_data["totals"],
            self.stage_types_data["users"]
        ) = StageTypesDataManager(
            self.export_manager.subsidy_period
        ).get_data()

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_circles()
        self.export_stage()

        return self.export_manager.return_document("detalls_acompanyaments")

    def export_stage(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet("Itinerari")
        self.export_manager.row_number = 1

        columns = [
            ("Tipus d'acompanyament justifica.", 40),
            ("Hores executades", 20),
            ("Hores justificades", 20),
            ("Hores sense certificat", 20),
            ("Percentatge", 20),
        ]
        self.export_manager.create_columns(columns)
        self.stage_totals_rows()
        self.stage_users_rows()

    def stage_totals_rows(self):
        first_row = self.export_manager.row_number
        rows_number = len(self.stage_types_data["totals"])
        for row in self.stage_types_data["totals"]:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row["totals"])
            self.set_percent_cell(first_row, rows_number)

    def stage_users_rows(self):
        for stage_type in self.stage_types_data["users"].values():
            stage_type_v_name = stage_type["verbose_name"]
            for stage_subtype in stage_type["subtypes"].values():
                if not len(stage_subtype["users"]):
                    continue
                stage_subtype_v_name = stage_subtype["verbose_name"]
                row = [
                    f"{stage_type_v_name} - {stage_subtype_v_name}",
                    "Número de sessions",
                    "Hores justificades",
                    "Hores sense certificat",
                    "Percentatge"
                ]
                self.export_manager.row_number += 2
                self.export_manager.fill_row_data(row)
                self.export_manager.format_row_header()
                first_row = self.export_manager.row_number
                rows_number = len(stage_subtype["users"])
                for row in stage_subtype["users"]:
                    self.export_manager.row_number += 1
                    self.export_manager.fill_row_data(row)
                    self.set_percent_cell(first_row, rows_number)

    def set_percent_cell(self, first_row, rows_number):
        last_row = first_row + rows_number
        cur_row = self.export_manager.row_number
        f_total_sum = f"SUM(C{first_row}:D{last_row})"
        f_user_sum = f"SUM(C{cur_row}:D{cur_row})"
        f = f"={f_user_sum}/{f_total_sum}"
        self.export_manager.format_cell(
            5,
            cur_row,
            "number_format",
            FORMAT_PERCENTAGE
        )
        self.export_manager.set_cell_value(5, cur_row, f)
        self.export_manager.format_cell_default_font(5, cur_row)

    def export_circles(self):
        self.export_manager.worksheet.title = "Ateneu-Cercles"
        self.export_manager.row_number = 1

        columns = [
            (CirclesChoices.CERCLE0.label_named, 40),
            ("Bases Convo", 20),
            ("Justificades BO", 20),
            ("Sense certificat BO", 20),
        ]
        self.export_manager.create_columns(columns)
        self.circle_n_rows(CirclesChoices.CERCLE0)
        self.circle_headers(CirclesChoices.CERCLE1.label_named)
        self.circle_n_rows(CirclesChoices.CERCLE1)
        self.circle_headers(CirclesChoices.CERCLE2.label_named)
        self.circle_n_rows(CirclesChoices.CERCLE2)
        self.circle_headers(CirclesChoices.CERCLE3.label_named)
        self.circle_n_rows(CirclesChoices.CERCLE3)
        self.circle_headers(CirclesChoices.CERCLE4.label_named)
        self.circle_n_rows(CirclesChoices.CERCLE4)
        self.circle_headers(CirclesChoices.CERCLE5.label_named)
        self.circle_n_rows(CirclesChoices.CERCLE5)
        self.circles_ateneu_user_rows()

    def circle_headers(self, name):
        self.export_manager.row_number += 1
        row = [
            name,
            "Bases Convo",
            "Justificades BO",
            "Sense certificat BO",
        ]
        self.export_manager.row_number += 1
        self.export_manager.fill_row_data(row)
        self.export_manager.format_row_header()

    def circle_n_rows(self, circle):

        rows = self.circles_data[circle.name].values()
        for row in rows:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row)

    def circles_ateneu_user_rows(self):
        for data in self.users_data.values():
            verbose_name, values = data.values()
            self.export_manager.row_number += 2
            row = [
                verbose_name,
                "Número de SESSIONS",
                "Hores justificades",
                "Hores sense certificat",
            ]
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row)
            self.export_manager.format_row_header()

            for row in values:
                self.export_manager.row_number += 1
                self.export_manager.fill_row_data(row)


class StageDetailsDataManager:
    subsidy_period = None

    def __init__(self, subsidy_period):
        self.subsidy_period = subsidy_period

    @staticmethod
    def none_as_zero(value):
        return value if value else 0


class StageTypesDataManager(StageDetailsDataManager):
    """
    stage_subtypes will be populated with this scheme:
    {1: 'Acollida', 2: 'Procés', 3: 'Constitució', 4: 'Acompanyament'}
    """
    stage_types = {
        11: {
            "verbose_name": "Creació",
            "name": "creation",
        },
        12: {
            "verbose_name": "Consolidació",
            "name": "consolidation",
        },
    }
    stage_subtypes = {}

    def __init__(self, *args):
        super().__init__(*args)
        qs = StageSubtype.objects.all()
        for subtype in qs:
            self.stage_subtypes.update({
                subtype.pk: subtype.name
            })
        self.stage_subtypes.update({
            0: "Sense subtipus"
        })

    def get_data(self):
        creation_totals_data = self.get_totals_data(
            self.stage_types[11]
        )
        consolidation_totals_data = self.get_totals_data(
            self.stage_types[12]
        )
        totals_data = creation_totals_data + consolidation_totals_data
        users_data = self.get_users_data()
        users_data = self.format_users_data(users_data)
        return totals_data, users_data

    def get_users_data_scheme(self):
        """
        :return: dict with this scheme:
                data = {
            11: {
                "verbose_name": "Foo",
                "name": "foo",
                "subtypes": {
                    4: [ ],
                    5 [ ],
                }
            },
            12: {
                "verbose_name": "Foo",
                "name": "foo",
                "subtypes": {
                    4: [ ],
                    5 [ ],
                }
            },
        }
        """
        data = self.stage_types
        for stage_type_key in data.keys():
            data[stage_type_key].update({
                "subtypes": {}
            })
            for stage_subtype in self.stage_subtypes.keys():
                data[stage_type_key]["subtypes"].update({
                    stage_subtype: {
                        "verbose_name": self.stage_subtypes[stage_subtype],
                        "users": []
                    }
                })
        return data

    def format_users_data(self, users_data):
        """
        :param users_data: queryset obtained from get_users_data()
        :return: the dictionary from get_users_data_scheme() filled like this:
        data = {
            11: {
                "verbose_name": "Stage Name",
                "name": "stage_name",
                "subtypes": {
                    4: {
                        "verbose_name": "Stage Subtype Name",
                        "users": [
                            ["Nom user", num_sessions, h_certificades, h_no_cert, percentage ],
                            ["Nom user 2", num_sessions, h_certificades,h_no_cert, percentage ],
                            ["Nom user 3", num_sessions, h_certificades,h_no_cert, percentage ],
                        ],
                    },
                    5: {
                        "verbose_name": "Stage Subtype Name",
                        "users": [
                            ["Nom user", num_sessions, h_certificades, h_no_cert, percentage ],
                            ["Nom user 2", num_sessions, h_certificades,h_no_cert, percentage ],
                            ["Nom user 3", num_sessions, h_certificades,h_no_cert, percentage ],
                        ],
                    },
                },
            },
            12: {
                [[ same structure ]]
            },
        }
        """
        data = self.get_users_data_scheme()
        for user in users_data:
            s_type = int(user["project_stage__stage_type"])
            if s_type not in self.stage_types:
                continue
            s_type_name = self.stage_types[s_type]["name"]
            s_subtype = int(user["project_stage__stage_subtype"]) \
                if user["project_stage__stage_subtype"] else 0

            if not user["session_responsible__first_name"]:
                user["session_responsible__first_name"] = "(sense nom)"
            subset = [
                user["session_responsible__first_name"],
                self.none_as_zero(
                    user["sessions_number"]
                ),
                self.none_as_zero(
                    user.get(
                        f"hours_{s_type_name}_{s_subtype}_certified",
                        "n/a"
                    )
                ),
                self.none_as_zero(
                    user.get(
                        f"hours_{s_type_name}_{s_subtype}_uncertified",
                        "n/a",
                    )
                ),
                0,
            ]
            data[s_type]["subtypes"][s_subtype]["users"].append(subset)
        return data

    def get_users_data(self):
        query = {}
        for stage_id, stage_type in self.stage_types.items():
            stage_name = stage_type["name"]
            for subtype_id in self.stage_subtypes.keys():
                query.update({
                    "sessions_number": Count('session_responsible'),
                    f"hours_{stage_name}_{subtype_id}_certified": Sum(
                        'hours',
                        filter=(
                            Q(project_stage__stage_type=stage_id) &
                            Q(project_stage__stage_subtype=subtype_id) &
                            ~Q(project_stage__scanned_certificate__in=["", None])
                        )
                    ),
                    f"hours_{stage_name}_{subtype_id}_uncertified": Sum(
                        'hours',
                        filter=(
                            Q(project_stage__stage_type=stage_id) &
                            Q(project_stage__stage_subtype=subtype_id) &
                            Q(project_stage__scanned_certificate__in=["", None])
                        )
                    ),
                })
        qs = ProjectStageSession.objects.filter(
            project_stage__subsidy_period=self.subsidy_period,
        )
        qs = (
            qs
                .values(
                    "session_responsible__first_name",
                    "session_responsible__last_name",
                    "project_stage__stage_subtype",
                    "project_stage__stage_subtype__name",
                    "project_stage__stage_type",
                )
                .annotate(**query)
        )
        qs = qs.order_by()
        data = qs
        return data

    def get_totals_data(self, stage_type):
        stage_type_name = stage_type["name"]
        query = {
            f"hours_{stage_type_name}_certified": Sum(
                "stage_sessions__hours",
                filter=(
                    ~Q(scanned_certificate__in=["", None])
                )
            ),
            f"hours_{stage_type_name}_uncertified": Sum(
                "stage_sessions__hours",
                filter=(
                    Q(scanned_certificate__in=["", None])
                )
            ),
        }
        qs = ProjectStage.objects.filter(
            subsidy_period=self.subsidy_period,
            stage_type=11,
        )
        qs = (
            qs
                .values('stage_subtype')
                .annotate(**query)
        )
        qs = qs.order_by()
        data = self.format_totals_data(stage_type, qs)
        return data

    def format_totals_data(self, stage_type, qs):
        """
        IDEA:
        Aprofitar que el query que ja tenim ara genera totes les combinacions de:
        creation - Acollida
        creation - Procés
        creation - Constitució
        consolidation - Acollida
        consolidation - Acompanyament
        :return:
        """
        data = []
        for item in qs:
            data.append({
                "totals": self.fill_total_row(stage_type, item),
                "users": [],
            })
        return data

    def fill_total_row(self, stage_type, item):
        cert = self.none_as_zero(
            item[f"hours_{stage_type['name']}_certified"]
        )
        uncert = self.none_as_zero(
            item[f"hours_{stage_type['name']}_uncertified"]
        )
        subtype_name = self.stage_subtypes.get(item['stage_subtype'], "(cap)")
        return [
            f"{stage_type['verbose_name']} - {subtype_name}",
            cert + uncert,
            cert,
            uncert,
            0,  # TODO: Percentage
        ]


class CirclesPerUserDataManager(StageDetailsDataManager):
    def get_data(self):
        query = {
            'sessions_number': Count('session_responsible'),
            **self.get_circle_queryset(CirclesChoices.CERCLE0),
            **self.get_circle_queryset(CirclesChoices.CERCLE1),
            **self.get_circle_queryset(CirclesChoices.CERCLE2),
            **self.get_circle_queryset(CirclesChoices.CERCLE3),
            **self.get_circle_queryset(CirclesChoices.CERCLE4),
            **self.get_circle_queryset(CirclesChoices.CERCLE5),
        }
        qs = ProjectStageSession.objects.filter(
            project_stage__subsidy_period=self.subsidy_period,
        )
        qs = (
            qs
                .values(
                    "session_responsible__id",
                    "session_responsible__first_name"
                )
                .annotate(**query)
        )
        qs = qs.order_by()
        data = self.format_data(qs)
        return data

    def get_circle_queryset(self, circle):
        return {
            f'hours_{circle.name}_certified': Sum(
                'hours',
                filter=(
                        Q(project_stage__circle=circle) &
                        Q(project_stage__scanned_certificate__isnull=False) &
                        ~Q(project_stage__scanned_certificate__exact='')
                )
            ),
            f'hours_{circle.name}_uncertified': Sum(
                'hours',
                filter=(
                        Q(project_stage__circle=circle) &
                        Q(project_stage__scanned_certificate__isnull=True) |
                        Q(project_stage__scanned_certificate__exact='')
                )
            ),
        }

    @staticmethod
    def get_base_data_structure():
        return {
            CirclesChoices.CERCLE0.name: {
                "verbose_name": CirclesChoices.CERCLE0.label_named,
                "values": [],
            },
            CirclesChoices.CERCLE1.name: {
                "verbose_name": CirclesChoices.CERCLE1.label_named,
                "values": [],
            },
            CirclesChoices.CERCLE2.name: {
                "verbose_name": CirclesChoices.CERCLE2.label_named,
                "values": [],
            },
            CirclesChoices.CERCLE3.name: {
                "verbose_name": CirclesChoices.CERCLE3.label_named,
                "values": [],
            },
            CirclesChoices.CERCLE4.name: {
                "verbose_name": CirclesChoices.CERCLE4.label_named,
                "values": [],
            },
            CirclesChoices.CERCLE5.name: {
                "verbose_name": CirclesChoices.CERCLE5.label_named,
                "values": [],
            },
        }

    def fill_user_data(self, circle, item):
        return [
            item["session_responsible__first_name"],
            self.none_as_zero(
                item["sessions_number"]
            ),
            self.none_as_zero(
                item[f"hours_{circle}_certified"]
            ),
            self.none_as_zero(
                item[f"hours_{circle}_uncertified"]
            ),
        ]

    def format_data(self, data):
        base_template = self.get_base_data_structure()
        circles = [x for x in base_template.keys()]
        for item in data:
            if not item["session_responsible__id"]:
                item["session_responsible__first_name"] = "(sense usuari)"
            for circle in circles:
                base_template[circle]["values"].append(
                    self.fill_user_data(circle, item)
                )
        return base_template


class CirclesDataManager(StageDetailsDataManager):
    def get_data_structure(self):
        return {
            **self.get_data_structure_for_circle(CirclesChoices.CERCLE0),
            **self.get_data_structure_for_circle(CirclesChoices.CERCLE1),
            **self.get_data_structure_for_circle(CirclesChoices.CERCLE2),
            **self.get_data_structure_for_circle(CirclesChoices.CERCLE3),
            **self.get_data_structure_for_circle(CirclesChoices.CERCLE4),
            **self.get_data_structure_for_circle(CirclesChoices.CERCLE5),
        }

    def get_data_structure_for_circle(self, circle):
        return {
            circle.name: {
                **self.get_data_structure_for_service(
                    "total",
                    "Total hores",
                ),
                **self.get_data_structure_for_service(
                    ServicesChoices.MAP_DIAGNOSI.name,
                    ServicesChoices.MAP_DIAGNOSI.label,
                ),
                **self.get_data_structure_for_service(
                    ServicesChoices.DIV_SENS_GEN_CONEIXEMENT.name,
                    ServicesChoices.DIV_SENS_GEN_CONEIXEMENT.label,
                ),
                **self.get_data_structure_for_service(
                    ServicesChoices.FORM_PROM_CREA_CONS.name,
                    ServicesChoices.FORM_PROM_CREA_CONS.label,
                ),
                **self.get_data_structure_for_service(
                    ServicesChoices.ACOM_CREA_CONS.name,
                    ServicesChoices.ACOM_CREA_CONS.label,
                ),
                **self.get_data_structure_for_service(
                    ServicesChoices.INTERCOOP_XARXA_TERRITORI.name,
                    ServicesChoices.INTERCOOP_XARXA_TERRITORI.label,
                ),
                **self.get_data_structure_for_service(
                    ServicesChoices.PUNT_INFO.name,
                    ServicesChoices.PUNT_INFO.label,
                ),
                **self.get_data_structure_for_service(
                    None,
                    "Sense Servei",
                ),
                **self.get_data_structure_for_service(
                    "insertions",
                    "Insercions",
                ),
                **self.get_data_structure_for_service(
                    "constituted",
                    "Constitució",
                ),
            }
        }

    def get_data_structure_for_service(self, name, label):
        return {
            name: [
                label,
                0,  # Nº que haurà de venir de les bases convocatòria.
                0,  # Justificades
                0,  # Sense certificat
            ]
        }

    def get_circles_data(self):
        query = {
            **self.get_circles_data_queryset(CirclesChoices.CERCLE0),
            **self.get_circles_data_queryset(CirclesChoices.CERCLE1),
            **self.get_circles_data_queryset(CirclesChoices.CERCLE2),
            **self.get_circles_data_queryset(CirclesChoices.CERCLE3),
            **self.get_circles_data_queryset(CirclesChoices.CERCLE4),
            **self.get_circles_data_queryset(CirclesChoices.CERCLE5),
        }
        qs = ProjectStage.objects.filter(
            subsidy_period=self.subsidy_period,
        )
        qs = (
            qs
                .values('service')
                .annotate(**query)
        )
        # Disabling order_by because it breaks the group_by.
        qs = qs.order_by()
        data = self.format_circles_data(qs)
        return data

    def get_circles_data_queryset(self, circle):
        return {
            f'hours_{circle.name}_certified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(circle=circle) &
                    ~Q(scanned_certificate__in=['', None])
                )
            ),
            f'hours_{circle.name}_uncertified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(circle=circle) &
                    Q(scanned_certificate__in=['', None])
                )
            ),
        }

    def format_circles_data(self, data):
        template = self.get_data_structure()
        for item in data:
            self.format_circles_data_item(template, CirclesChoices.CERCLE0, item)
            self.format_circles_data_item(template, CirclesChoices.CERCLE1, item)
            self.format_circles_data_item(template, CirclesChoices.CERCLE2, item)
            self.format_circles_data_item(template, CirclesChoices.CERCLE3, item)
            self.format_circles_data_item(template, CirclesChoices.CERCLE4, item)
            self.format_circles_data_item(template, CirclesChoices.CERCLE5, item)

        return template

    def format_circles_data_item(self, template, circle, item):
        service_name = (
            ServicesChoices(item["service"]).name if item["service"]
            else item["service"]
        )
        template[circle.name][service_name][2] = self.none_as_zero(
                item.get(f"hours_{circle.name}_certified")
            )
        template[circle.name][service_name][3] = self.none_as_zero(
            item[f"hours_{circle.name}_uncertified"]
        )
        if isinstance(item[f"hours_{circle.name}_certified"], numbers.Number):
            template[circle.name]["total"][2] += item[f"hours_{circle.name}_certified"]
        if isinstance(item[f"hours_{circle.name}_uncertified"], numbers.Number):
            template[circle.name]["total"][3] += item[f"hours_{circle.name}_uncertified"]
