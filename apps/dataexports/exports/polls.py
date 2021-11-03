from statistics import mean

from django.db.models import (
    Count, Avg, IntegerField, Case, When, Sum,
    Value
)

from cc_courses.models import Organizer, Activity
from coopolis.models import ActivityPoll
from coopolis_backoffice.settings import AXIS_OPTIONS
from dataexports.exports.exceptions import (
    MissingOrganizers,
    AxisDoesNotExistException
)
from dataexports.exports.manager import ExcelExportManager
from dataexports.exports.row_factories import (
    EmptyRow, TextWithValue,
    TitleRow, TextWithYesNoEmpty, GlobalReportRow, GlobalReportYesNoEmptyRow,
    TextRow
)


class ExportPolls:
    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.organizers = dict()
        self.import_organizers()
        if not len(self.organizers):
            raise MissingOrganizers

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.global_report()
        for axis in AXIS_OPTIONS:
            self.global_report(axis[0])
        self.answers_list("also_interested_in", "AltresTemesInterès")
        self.answers_list("heard_about_it", "ComUsHeuAssabentat")
        self.answers_list("comments", "VolsComentarAlgunaCosaMés")
        self.all_activities()

        return self.export_manager.return_document("resultats_enquestes")

    def all_activities(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "BuidatTotal"
        )
        self.export_manager.row_number = 1
        columns = [
            ("Totals per sessió", 60),
            ("", 20),
        ]
        self.export_manager.create_columns(columns)
        self.all_activities_rows()

    def all_activities_obj(self):
        return (
            Activity
            .objects
            .filter(
                date_start__range=self.export_manager.subsidy_period_range,
            )
            .exclude(polls=None)
            .annotate(
                Avg("polls__duration"),
                Avg("polls__hours"),
                Avg("polls__information"),
                Avg("polls__on_schedule"),
                Avg("polls__included_resources"),
                Avg("polls__space_adequation"),
                Avg("polls__contents"),
                Avg("polls__methodology_fulfilled_objectives"),
                Avg("polls__methodology_better_results"),
                Avg("polls__participation_system"),
                Avg("polls__teacher_has_knowledge"),
                Avg("polls__teacher_resolved_doubts"),
                Avg("polls__teacher_has_communication_skills"),
                Avg("polls__expectations_satisfied"),
                Avg("polls__adquired_new_tools"),
                Avg("polls__general_satisfaction"),
                Count("polls"),
                met_new_people_yes=Sum(
                    Case(
                        When(polls__met_new_people=True, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    )
                ),
                met_new_people_no=Sum(
                    Case(
                        When(polls__met_new_people=False, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    ),
                ),
                met_new_people_empty=Sum(
                    Case(
                        When(polls__met_new_people=None, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    )
                ),
                wanted_start_cooperative_yes=Sum(
                    Case(
                        When(polls__wanted_start_cooperative=True, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    )
                ),
                wanted_start_cooperative_no=Sum(
                    Case(
                        When(polls__wanted_start_cooperative=False, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    ),
                ),
                wanted_start_cooperative_empty=Sum(
                    Case(
                        When(polls__wanted_start_cooperative=None, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    )
                ),
                wants_start_cooperative_now_yes=Sum(
                    Case(
                        When(polls__wants_start_cooperative_now=True, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    )
                ),
                wants_start_cooperative_now_no=Sum(
                    Case(
                        When(polls__wants_start_cooperative_now=False, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    ),
                ),
                wants_start_cooperative_now_empty=Sum(
                    Case(
                        When(polls__wants_start_cooperative_now=None, then=Value(1)),
                        output_field=IntegerField(),
                        default=0,
                    )
                ),
            )
        )

    def all_activities_rows(self):
        obj = self.all_activities_obj()
        for activity in obj:
            rows = [
                EmptyRow(),
                EmptyRow(),
                TextWithValue("Nom de l'actuació", activity.name),
                TextWithValue("Eix", activity.axis),
                TextWithValue(
                    "Tipus d'actuació",
                    "Per menors" if activity.for_minors else "Per adults",
                ),
                TextWithValue(
                    "Cercle / Ateneu",
                    activity.organizer.name if activity.organizer else "-",
                ),
                TextWithValue(
                    "Municipi",
                    activity.place.town.name if activity.place and activity.place.town else "-",
                ),
                TextWithValue(
                    "Nombre de participants",
                    len(activity.enrolled.all()),
                ),
                TextWithValue(
                    "Nombre d'enquestes rebudes",
                    activity.polls__count,
                ),
                TitleRow("Organització"),
                TextWithValue("Durada", activity.polls__duration__avg),
                TextWithValue(
                    "La durada ha estat l'adequada?",
                    activity.polls__duration__avg,
                ),
                TextWithValue(
                    "Els horaris han estat adequats?",
                    activity.polls__hours__avg,
                ),
                TextWithValue(
                    "Informació necessària per fer l'activitat",
                    activity.polls__information__avg,
                ),
                TextWithValue(
                    "S'han complert les dates, horaris, etc...",
                    activity.polls__on_schedule__avg,
                ),
                TextWithValue(
                    "Materials de suport facilitats",
                    activity.polls__included_resources__avg,
                ),
                TextWithValue(
                    "Els espais han estat adequats (sales, aules, plataforma digital...)",
                    activity.polls__space_adequation__avg,
                ),
                TitleRow("Continguts"),
                TextWithValue(
                    "Els continguts han estat adequats",
                    activity.polls__contents__avg,
                ),
                TitleRow("Metodologia"),
                TextWithValue(
                    "La metodologia ha estat coherent amb els objectius",
                    activity.polls__methodology_fulfilled_objectives__avg,
                ),
                TextWithValue(
                    "La metodologia ha permès obtenir millors resultats",
                    activity.polls__methodology_better_results__avg,
                ),
                TextWithValue(
                    "El sistema de participació i resolució de dubtes ha estat adequat?",
                    activity.polls__participation_system__avg,
                ),
                TitleRow("Valoració de la persona formadora"),
                TextWithValue(
                    "Ha mostrat coneixements i experiència sobre el tema?",
                    activity.polls__teacher_has_knowledge__avg,
                ),
                TextWithValue(
                    "Ha aconseguit resoldre els problemes i dubtes que s’ha plantejat?",
                    activity.polls__teacher_resolved_doubts__avg,
                ),
                TextWithValue(
                    "El professional ha mostrat competències comunicatives?",
                    activity.polls__teacher_has_communication_skills__avg,
                ),
                TitleRow("Utilitat del curs"),
                TextWithValue(
                    "Ha satisfet les meves expectatives",
                    activity.polls__expectations_satisfied__avg,
                ),
                TextWithValue(
                    "He incorporat eines per aplicar a nous projectes",
                    activity.polls__adquired_new_tools__avg,
                ),
                TextWithYesNoEmpty(
                    "M'ha permès conèixer persones afins",
                    (
                        activity.met_new_people_yes,
                        activity.met_new_people_no,
                        activity.met_new_people_empty,
                    ),
                ),
                TextWithYesNoEmpty(
                    "Abans del curs, teníeu ganes/necessitats d'engegar algun projecte cooperatiu",
                    (
                        activity.wanted_start_cooperative_yes,
                        activity.wanted_start_cooperative_no,
                        activity.wanted_start_cooperative_empty,
                    ),
                ),
                TextWithYesNoEmpty(
                    "I després?",
                    (
                        activity.wants_start_cooperative_now_yes,
                        activity.wants_start_cooperative_now_no,
                        activity.wants_start_cooperative_now_empty,
                    ),
                ),
                TitleRow("Valoració global"),
                TextWithValue(
                    "Grau de satisfacció general",
                    activity.polls__general_satisfaction__avg,
                ),

            ]

            for row in rows:
                self.export_manager.fill_row_from_factory(row)

    def answers_list(self, question, title):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            title
        )
        self.export_manager.row_number = 1
        columns = [
            ("Acumulació de respostes a aquesta pregunta", 80),
        ]
        self.export_manager.create_columns(columns)
        obj = self.answers_list_obj()
        self.answers_list_rows(obj, question)

    def answers_list_rows(self, obj, question):
        for poll_obj in obj:
            answer = getattr(poll_obj, question)
            if answer:
                self.export_manager.fill_row_from_factory(
                    TextRow(answer)
                )

    def answers_list_obj(self):
        return ActivityPoll.objects.filter(
            activity__date_start__range=self.export_manager.subsidy_period_range,
        )

    def global_report(self, axis: str = None):
        if axis:
            self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
                self.get_axis_title(axis)
            )
        else:
            # The first sheet is already created, just need to adjust name.
            self.export_manager.worksheet.title = "Informe Global"

        self.export_manager.row_number = 1

        columns = [
            ("", 60),
            (self.organizers.get(0), 20),
            (self.organizers.get(1), 20),
            (self.organizers.get(2), 20),
            (self.organizers.get(3), 20),
            (self.organizers.get(4), 20),
        ]
        self.export_manager.create_columns(columns)

        self.polls_rows(axis)

    def global_report_obj(self, axis: str = None):
        querysets = []
        for organizer in self.organizers.values():
            qs = ActivityPoll.objects.filter(
                    activity__date_start__range=self.export_manager.subsidy_period_range,
                    activity__organizer=organizer,
                )
            if axis:
                qs = qs.filter(activity__axis=axis)
            querysets.append(
                qs
            )
        # qs.annotate(Count("id"))
        # qs.order_by()
        averages = {
            "ateneu": self.get_averages_qs(querysets[0]),
            "cercle1": {},
            "cercle2": {},
            "cercle3": {},
            "cercle4": {},
        }
        total_organizers = len(self.organizers)
        if total_organizers > 1:
            averages["cercle1"] = self.get_averages_qs(querysets[1])
        if total_organizers > 2:
            averages["cercle2"] = self.get_averages_qs(querysets[2])
        if total_organizers > 3:
            averages["cercle3"] = self.get_averages_qs(querysets[3])
        if total_organizers > 4:
            averages["cercle4"] = self.get_averages_qs(querysets[4])

        return querysets, averages

    def get_averages_qs(self, queryset):
        return queryset.aggregate(
            Count("id"),
            Avg("duration"),
            Avg("hours"),
            Avg("information"),
            Avg("on_schedule"),
            Avg("included_resources"),
            Avg("space_adequation"),
            Avg("contents"),
            Avg("methodology_fulfilled_objectives"),
            Avg("methodology_better_results"),
            Avg("participation_system"),
            Avg("teacher_has_knowledge"),
            Avg("teacher_resolved_doubts"),
            Avg("teacher_has_communication_skills"),
            Avg("expectations_satisfied"),
            Avg("adquired_new_tools"),
            Avg("general_satisfaction"),
            global_average=(
                Avg("duration")
                + Avg("hours")
                + Avg("information")
                + Avg("on_schedule")
                + Avg("included_resources")
                + Avg("space_adequation")
                + Avg("contents")
                + Avg("methodology_fulfilled_objectives")
                + Avg("methodology_better_results")
                + Avg("participation_system")
                + Avg("teacher_has_knowledge")
                + Avg("teacher_resolved_doubts")
                + Avg("teacher_has_communication_skills")
                + Avg("expectations_satisfied")
                + Avg("adquired_new_tools")
                + Avg("general_satisfaction")
            ),
            met_new_people_yes=Sum(
                Case(
                    When(met_new_people=True, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
            met_new_people_no=Sum(
                Case(
                    When(met_new_people=False, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                ),
            ),
            met_new_people_empty=Sum(
                Case(
                    When(met_new_people=None, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
            wanted_start_cooperative_yes=Sum(
                Case(
                    When(wanted_start_cooperative=True, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
            wanted_start_cooperative_no=Sum(
                Case(
                    When(wanted_start_cooperative=False, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                ),
            ),
            wanted_start_cooperative_empty=Sum(
                Case(
                    When(wanted_start_cooperative=None, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
            wants_start_cooperative_now_yes=Sum(
                Case(
                    When(wants_start_cooperative_now=True, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
            wants_start_cooperative_now_no=Sum(
                Case(
                    When(wants_start_cooperative_now=False, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                ),
            ),
            wants_start_cooperative_now_empty=Sum(
                Case(
                    When(wants_start_cooperative_now=None, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
        )

    def polls_rows(self, axis: str = None):
        querysets, averages = self.global_report_obj(axis)
        rows = [
            GlobalReportRow(
                "Nombre d'enquestes de satisfacció valorades",
                averages["ateneu"]["id__count"],
                averages["cercle1"]["id__count"],
                averages["cercle2"]["id__count"],
                averages["cercle3"]["id__count"],
                averages["cercle4"]["id__count"],
            ),
            EmptyRow(),
            TitleRow(
                "Valoracions globals",
            ),
            GlobalReportRow(
                "Valoració global de les actuacions",
                self.get_global_average(averages["ateneu"]),
                self.get_global_average(averages["cercle1"]),
                self.get_global_average(averages["cercle2"]),
                self.get_global_average(averages["cercle3"]),
                self.get_global_average(averages["cercle4"]),
            ),
            EmptyRow(),
            TitleRow("Organització"),
            GlobalReportRow(
                "La durada ha estat l'adequada?",
                values_dict=averages,
                values_dict_field="duration__avg",
            ),
            GlobalReportRow(
                "Els horaris han estat adequats?",
                values_dict=averages,
                values_dict_field="hours__avg",
            ),
            GlobalReportRow(
                "Informació necessària per fer l'activitat",
                values_dict=averages,
                values_dict_field="information__avg",
            ),
            GlobalReportRow(
                "S'han complert les dates, horaris, etc...",
                values_dict=averages,
                values_dict_field="on_schedule__avg",
            ),
            GlobalReportRow(
                "Materials de suport facilitats",
                values_dict=averages,
                values_dict_field="included_resources__avg",
            ),
            GlobalReportRow(
                "Els espais han estat adequats (sales, aules, plataforma digital...)",
                values_dict=averages,
                values_dict_field="space_adequation__avg",
            ),
            EmptyRow(),
            TitleRow("Continguts"),
            GlobalReportRow(
                "Els continguts han estat adequats",
                values_dict=averages,
                values_dict_field="contents__avg",
            ),
            TitleRow("Metodologia"),
            GlobalReportRow(
                "La metodologia ha estat coherent amb els objectius",
                values_dict=averages,
                values_dict_field="methodology_fulfilled_objectives__avg",
            ),
            GlobalReportRow(
                "La metodologia ha permès obtenir millors resultats",
                values_dict=averages,
                values_dict_field="methodology_better_results__avg",
            ),
            GlobalReportRow(
                "El sistema de participació i resolució de dubtes ha estat adequat?",
                values_dict=averages,
                values_dict_field="participation_system__avg",
            ),
            EmptyRow(),
            TitleRow("Valoració de la persona formadora"),
            GlobalReportRow(
                "Ha mostrat coneixements i experiència sobre el tema?",
                values_dict=averages,
                values_dict_field="teacher_has_knowledge__avg",
            ),
            GlobalReportRow(
                "Ha aconseguit resoldre els problemes i dubtes que s’ha plantejat?",
                values_dict=averages,
                values_dict_field="teacher_resolved_doubts__avg",
            ),
            GlobalReportRow(
                "El professional ha mostrat competències comunicatives?",
                values_dict=averages,
                values_dict_field="teacher_has_communication_skills__avg",
            ),
            EmptyRow(),
            TitleRow("Utilitat del curs"),
            GlobalReportRow(
                "Ha satisfet les meves expectatives",
                values_dict=averages,
                values_dict_field="expectations_satisfied__avg",
            ),
            GlobalReportRow(
                "He incorporat eines per aplicar a nous projectes",
                values_dict=averages,
                values_dict_field="adquired_new_tools__avg",
            ),
            GlobalReportYesNoEmptyRow(
                "M'ha permès conèixer persones afins",
                (
                    averages["ateneu"].get("met_new_people_yes"),
                    averages["ateneu"].get("met_new_people_no"),
                    averages["ateneu"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle1"].get("met_new_people_yes"),
                    averages["cercle1"].get("met_new_people_no"),
                    averages["cercle1"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle2"].get("met_new_people_yes"),
                    averages["cercle2"].get("met_new_people_no"),
                    averages["cercle2"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle3"].get("met_new_people_yes"),
                    averages["cercle3"].get("met_new_people_no"),
                    averages["cercle3"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle4"].get("met_new_people_yes"),
                    averages["cercle4"].get("met_new_people_no"),
                    averages["cercle4"].get("met_new_people_empty"),
                ),
            ),
            GlobalReportYesNoEmptyRow(
                "Abans del curs, teníeu ganes/necessitats d'engegar algun projecte cooperatiu",
                (
                    averages["ateneu"].get("wanted_start_cooperative_yes"),
                    averages["ateneu"].get("wanted_start_cooperative_no"),
                    averages["ateneu"].get("wanted_start_cooperative_empty"),
                ),
                (
                    averages["cercle1"].get("wanted_start_cooperative_yes"),
                    averages["cercle1"].get("wanted_start_cooperative_no"),
                    averages["cercle1"].get("wanted_start_cooperative_empty"),
                ),
                (
                    averages["cercle2"].get("wanted_start_cooperative_yes"),
                    averages["cercle2"].get("wanted_start_cooperative_no"),
                    averages["cercle2"].get("wanted_start_cooperative_empty"),
                ),
                (
                    averages["cercle3"].get("wanted_start_cooperative_yes"),
                    averages["cercle3"].get("wanted_start_cooperative_no"),
                    averages["cercle3"].get("wanted_start_cooperative_empty"),
                ),
                (
                    averages["cercle4"].get("wanted_start_cooperative_yes"),
                    averages["cercle4"].get("wanted_start_cooperative_no"),
                    averages["cercle4"].get("wanted_start_cooperative_empty"),
                ),
            ),
            GlobalReportYesNoEmptyRow(
                "I després?",
                (
                    averages["ateneu"].get("wants_start_cooperative_now_yes"),
                    averages["ateneu"].get("wants_start_cooperative_now_no"),
                    averages["ateneu"].get("wants_start_cooperative_now_empty"),
                ),
                (
                    averages["cercle1"].get("wants_start_cooperative_now_yes"),
                    averages["cercle1"].get("wants_start_cooperative_now_no"),
                    averages["cercle1"].get("wants_start_cooperative_now_empty"),
                ),
                (
                    averages["cercle2"].get("wants_start_cooperative_now_yes"),
                    averages["cercle2"].get("wants_start_cooperative_now_no"),
                    averages["cercle2"].get("wants_start_cooperative_now_empty"),
                ),
                (
                    averages["cercle3"].get("wants_start_cooperative_now_yes"),
                    averages["cercle3"].get("wants_start_cooperative_now_no"),
                    averages["cercle3"].get("wants_start_cooperative_now_empty"),
                ),
                (
                    averages["cercle4"].get("wants_start_cooperative_now_yes"),
                    averages["cercle4"].get("wants_start_cooperative_now_no"),
                    averages["cercle4"].get("wants_start_cooperative_now_empty"),
                ),
            ),
            EmptyRow(),
            TitleRow("Valoració global"),
            GlobalReportRow(
                "Grau de satisfacció general",
                values_dict=averages,
                values_dict_field="general_satisfaction__avg",
            ),
        ]

        for row in rows:
            self.export_manager.fill_row_from_factory(row)

    def import_organizers(self):
        orgs = Organizer.objects.all()
        i = 0
        for org in orgs:
            self.organizers.update({
                i: org
            })
            i += 1

    def get_global_average(self, values: dict):
        averageable_fields = [
            "duration__avg",
            "hours__avg",
            "information__avg",
            "on_schedule__avg",
            "included_resources__avg",
            "space_adequation__avg",
            "contents__avg",
            "methodology_fulfilled_objectives__avg",
            "methodology_better_results__avg",
            "participation_system__avg",
            "teacher_has_knowledge__avg",
            "teacher_resolved_doubts__avg",
            "teacher_has_communication_skills__avg",
            "expectations_satisfied__avg",
            "adquired_new_tools__avg",
            "general_satisfaction__avg",
        ]
        numbers = [
            x
            for key, x in values.items()
            if key in averageable_fields
               and x is not None
        ]
        if numbers:
            return mean(numbers)
        return 0

    def get_axis_title(self, axis):
        for axis_tuple in AXIS_OPTIONS:
            if axis in axis_tuple:
                return axis_tuple[1]
        raise AxisDoesNotExistException
