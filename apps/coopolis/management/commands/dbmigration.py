# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.db import connections
from django.core.management.base import BaseCommand
from collections import namedtuple
from coopolis.models import Project, User, Town
from cc_courses.models import Course, Activity, CoursePlace
from django.forms.models import model_to_dict
from django.core.management.commands.flush import Command as Flush
import re
from datetime import datetime


class Command(BaseCommand):
    help = 'Queries the information from the old Coòpolis backoffice to import it to the new one.'

    def handle(self, *args, **options):
        print("PROTECTED!")
        return
        Flush().handle(interactive=False, database="default", **options)
        tuples = manual_tuple()
        self.importprojects(tuples)
        self.importtowns()
        self.importusers(tuples)
        self.importplaces()
        self.importcourses()
        self.importactivities()
        self.importenrollments()

    def importenrollments(self):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM WORKSHOPPERSON ORDER BY ID")
            results = namedtuplefetchall(cursor)
            for result in results:
                # TODO: BÀSICAMENT, volcar les IDs dels 2 camps a la taula de enrolled.
                # Ho podem fer objecte per objecte i que generi la seva auto id.
                with connections['default'].cursor() as insert:
                    insert.execute("INSERT INTO "
                                   "cc_courses_activity_enrolled(activity_id, user_id) "
                                   "VALUES ("+str(result.workshopId)+", "+str(result.personId)+") "
                                   "ON CONFLICT DO NOTHING")
                print("Enrollment inserted. Old DB ID: "+str(result.ID))
            print("Imported: Inscripcions")

    def importcourses(self):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM EDUCATION ORDER BY ID")
            results = namedtuplefetchall(cursor)
            for result in results:
                print("Importing course, old database ID: "+str(result.ID))

                date_start = self.get_first_activity_date(result.ID)
                if date_start is None:
                    date_start = result.ORDINATIONDATE
                if date_start is None:
                    print("No starting day nor activities with a starting date, SKIPPING!")
                    continue

                row = Course(
                    id=result.ID,
                    title=result.TITLE,
                    slug=result.SLUG,
                    date_start=date_start,
                    date_end=None,
                    hours=result.SCHEDULESUMMARY,
                    description=result.SHORTOBJECTIVES,
                    published=True,
                    # Banner: pending to import!
                )
                row.save()
            self.synchronize_last_sequence(Course)
            print("Imported: Courses")

    def importplaces(self):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM GEOLOCATION ORDER BY ID")
            results = namedtuplefetchall(cursor)
            for result in results:
                print("Importing Place, old database ID: "+str(result.ID))

                row = CoursePlace(
                    id=result.ID,
                    name=result.NAME,
                    address=result.ADDRESS
                )
                row.save()
            self.synchronize_last_sequence(CoursePlace)
            print("Imported: Places")

    def importactivities(self):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM WORKSHOP ORDER BY ID")
            results = namedtuplefetchall(cursor)
            for result in results:
                to_skip = False
                print("Importing Activity, old database ID: "+str(result.ID))

                starting_time = self.parse_time(result.STARTTIME)
                if starting_time is None:
                    starting_time = datetime.strptime("11:00", "%H:%M")
                    print("Activity without Starting Time, set to 11:00. Title: "+result.TITLE)
                ending_time = self.parse_time(result.ENDTIME)
                if ending_time is None and starting_time is not None:
                    ending_time = self.create_ending_time(starting_time)

                course_id = result.education_id
                if course_id is None:
                    print("Activity without Course, CREATING COURSE. Title: "+result.TITLE)
                    new_course = self.create_course(result)
                    course_id = new_course.pk
                    print("New course ID: "+str(course_id))

                row = Activity(
                    id=result.ID,
                    course_id=course_id,
                    name=result.TITLE,
                    objectives=result.SHORTOBJECTIVES,
                    place_id=result.GEOLOCATION_ID,
                    date_start=result.DATE,
                    starting_time=starting_time,
                    ending_time=ending_time,
                    spots=result.PLACES,
                    # TODO: omplir el m2m dels ENROLLEDS, en una altra funció
                    organizer="AT",
                    entity=None,
                    axis=None,
                    published=True
                )
                row.save()
            self.synchronize_last_sequence(Activity)
            print("Imported: Activities")

    def importprojects(self, tuples):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM PROJECT")
            results = namedtuplefetchall(cursor)
            for result in results:
                print("Importing project, old database ID: "+str(result.ID))

                sector = "A"
                if result.SECTOR is not None:
                    sector = tuples["sector"][result.SECTOR][2]
                project_status = None
                if result.PROJECTSTATUS is not None:
                    project_status = tuples["project_status"][result.PROJECTSTATUS][1]
                motivation = None
                if result.INITIALDEMAND is not None:
                    motivation = tuples["initial_demand"][result.INITIALDEMAND][1]
                district = None
                if result.DISTRICT_ID is not None:
                    district = tuples["districts"][int(result.DISTRICT_ID)-1][1]
                cif = None
                if result.NIF is not None:
                    cif = result.NIF[:11]

                row = Project(
                    id=result.ID,
                    name=result.NAME[:200],
                    sector=sector,
                    web=result.WEB[:200],
                    project_status=project_status,
                    motivation=motivation,
                    mail=result.EMAIL,
                    phone=result.PHONE[:25],
                    district=district,
                    project_responsible=None,  # D'entrada serà sempre el mateix, falta saber l'ID de l'user.
                    number_people=result.NUMPEOPLE,
                    registration_date=result.REGISTRATIONDATE,
                    cif=cif,
                    subsidy_period=2018,
                    object_finality=result.PURPOSE,
                    project_origins=result.ORIGIN,
                    solves_necessities=result.RESOLVEDNEEDS,
                    social_base=result.SOCIALBASE
                    # TODO: Els 3 fitxers. Una opció és tirar peticions POST a /download.php amb
                    # user_hash: PERSON.WEBHASH
                    # url: http://localhost:8080/coopolis-backoffice-web-services/api/project/statutes
                )
                row.save()
        self.synchronize_last_sequence(Project)
        print("Imported: Projects")

    def importusers(self, tuples):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM v_exportacionomespersones ORDER BY idPersona")
            results = namedtuplefetchall(cursor)
            for result in results:
                print("Importing User, old database ID: "+str(result.idPersona))

                first_name = result.nom
                if first_name is None:
                    first_name = result.idPersona
                else:
                    first_name = first_name[:30]
                last_name = result.primerCognom
                if last_name is None:
                    last_name = result.idPersona
                gender = None
                if result.gènere is not None:
                    gender = tuples["gender"][result.gènere]
                birth_place = None
                if result.llocNaixement is not None:
                    birth_place = tuples["born_place"][result.llocNaixement]
                residence_district = None
                if result.idDistricte is not None:
                    residence_district = tuples["districts"][int(result.idDistricte)-1][1]
                phone_number = None
                if result.telèfon is not None:
                    phone_number = result.telèfon[:25]
                educational_level = None
                if result.nivellEstudis is not None:
                    educational_level = tuples["studies_level"][result.nivellEstudis]
                employment_situation = None
                if result.situacióLaboral is not None:
                    employment_situation = tuples["emplyment_situation"][result.situacióLaboral]
                discovered_us = None
                if result.asComEnsHaConegut is not None:
                    discovered_us = tuples["how_knew_us"][result.asComEnsHaConegut]

                row = User(
                    id=result.idPersona,
                    email=result.eMail,
                    first_name=first_name,
                    last_name=last_name,
                    surname2=result.segonCognom,
                    id_number=self.clear_dni(result.dni),
                    gender=gender,
                    birth_place=birth_place,
                    birthdate=result.dataNaixement,
                    residence_district=residence_district,
                    address=self.resolve_address(result.idPersona),
                    phone_number=phone_number,
                    educational_level=educational_level,
                    employment_situation=employment_situation,
                    discovered_us=discovered_us,
                    cooperativism_knowledge=result.coneixementsPrevis,
                )
                row.residence_town_id = result.idCiutat
                row.project_id = result.idProjecte
                row.save()
            self.synchronize_last_sequence(User)
            print("Imported: Users")

    def importtowns(self):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM TOWNSHIP ORDER BY ID")
            results = namedtuplefetchall(cursor)
            for result in results:
                print("Importing Town, old database ID: "+str(result.ID))
                row = Town(
                    id=result.ID,
                    name=result.DESCRIPTION
                )
                row.save()
            self.synchronize_last_sequence(Town)
            print("Imported: Towns.")

    def tests(self):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM ADDRESS")
            results = namedtuplefetchall(cursor)
            print(results[0].STREETNAME)

    def resolve_address(self, personID):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM ADDRESS WHERE person_id="+str(personID)+" ORDER BY ID LIMIT 1")
            results = namedtuplefetchall(cursor)
            if len(results) == 0:
                return None
            for result in results:
                address = None
                if result.STREETNAME is not None:
                    address = result.STREETNAME
                    if result.STREETTYPE is not None:
                        address = str(result.STREETTYPE)+" "+address
                    if result.STREETNUMBER is not None:
                        address = address+" "+str(result.STREETNUMBER)
                    if result.BLOCK is not None:
                        address = address+" "+str(result.BLOCK)
                    if result.FLOOR is not None:
                        address = address+" "+str(result.FLOOR)
                    if result.DOOR is not None:
                        address = address+" "+str(result.DOOR)
                return address

    def clear_dni(self, dni):
        return re.sub("[^a-zA-Z0-9]", "", dni)

    def synchronize_last_sequence(self, model):
        #  Postgresql aut-increments (called sequences) don't update the 'last_id' value if you manually specify an ID.
        #  This sets the last incremented number to the last id
        sequence_name = model._meta.db_table+"_"+model._meta.pk.name+"_seq"
        with connections['default'].cursor() as cursor:
            cursor.execute(
                "SELECT setval('" + sequence_name + "', (SELECT max(" + model._meta.pk.name + ") FROM " +
                model._meta.db_table + "))"
            )
        print("Last auto-incremental number for sequence "+sequence_name+" synchronized.")

    def get_first_activity_date(self, course_id):
        print("Resolving first activity date for Course ID: "+str(course_id))
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM WORKSHOP WHERE education_id=" + str(course_id) + " ORDER BY DATE LIMIT 1")
            results = namedtuplefetchall(cursor)
            if len(results) == 0:
                print("0 results, returning None")
                return None
            for result in results:
                print("Activity found, returning: "+str(result.DATE))
                return result.DATE

    def parse_time(self, time_string):
        if not time_string:
            return None
        clean_time_string = time_string.replace(".", ":").replace("h", "")
        if len(clean_time_string) < 3:
            clean_time_string = clean_time_string+":00"
        return datetime.strptime(clean_time_string, "%H:%M")

    def create_ending_time(self, starting_time):
        ending_time = datetime.strptime(str(starting_time.hour + 1) + ":" + str(starting_time.minute), "%H:%M")
        print(
            "Ending time None. Using starting time (" +
            str(starting_time.time()) + ") +1 hour (" +
            str(ending_time.time()) + ")")
        return ending_time

    def create_course(self, result):
        row = Course(
            title=result.TITLE,
            date_start=result.DATE,
            date_end=None,
            hours="De " + result.STARTTIME + " a " + result.ENDTIME,
            description=result.SHORTOBJECTIVES,
            published=True,
        )
        row.save()
        return row


def manual_tuple():
    return {
        "sector": (
            (0, 'FOOD', 'M'),
            (1, 'COUNSELING', 'S'),
            (2, 'COMUNICATION_TECHNOLOGY', 'C'),
            (3, 'CULTURE', 'C'),
            (4, 'CARE', 'U'),
            (5, 'EDUCATION', 'E'),
            (6, 'FINANCE', 'F'),
            (7, 'HOUSING', 'H'),
            (8, 'LOGISTIC', 'L'),
            (9, 'LEISURE', 'O'),
            (10, 'DRESSING', 'R'),
            (11, 'OTHER', 'A')
        ),
        "gender": (
            'FEMALE',
            'MALE',
            'OTHER',
        ),
        "studies_level": (
            'UNIVERSITY',
            'WITHOUT_STUDIES',
            'ELEMENTARY_SCHOOL',
            'HIGH_SCHOOL',
            'FP',
            'MASTER'
        ),
        "emplyment_situation": (
            'UNEMPLOYMENT_BENEFIT_RECEIVER',
            'UNEMPLOYMENT_BENEFIT_REQUESTED',
            'SELF_EMPLOYED',
            'EMPLOYED_WORKER',
        ),
        "legal_form": (
            (0, 'ASOCIATION'),
            (1, 'FOUNDATION'),
            (2, 'LIMITED_SOCIETY'),
            (3, 'ANONYMUS_SOCIETY'),
            (4, 'COOPERATIVE'),
            (5, 'CIVIL_SOCIETY'),
            (6, 'OTHER'),
            (7, 'NONE'),
        ),
        "project_status": (
            (0, 'IN_MEDITATION_PROCESS'),
            (1, 'IN_CONSTITUTION_PROCESS'),
            (2, 'RUNNING'),
        ),
        "initial_demand": (
            (0, 'COOPERATIVISM_EDUCATION'),
            (1, 'COOPERATIVE_CREATION'),
            (2, 'TRANSFORM_FROM_ASSOCIATION'),
            (3, 'TRANSFORM_FROM_SCP'),
            (4, 'ENTERPRISE_RELIEF'),
            (5, 'OTHER'),
        ),
        "born_place": (
            'BARCELONA',
            'CATALUNYA',
            'ESPANYA',
            'OTHER',
        ),
        "how_knew_us": (
            'PREVIOUS_ACTIVITY',
            'INTERNET',
            'FRIEND',
            'OTHER',
        ),
        "districts": (
            ('Ciutat Vella', 'CV'),
            ('Eixample', 'EX'),
            ('Horta-Guinardó', 'HG'),
            ('Les Corts', 'LC'),
            ('Nou Barris', 'NB'),
            ('Sant Andreu', 'SA'),
            ('Sant Martí', 'SM'),
            ('Sants-Montjuïc', 'ST'),
            ('Sarrià-Sant Gervasi', 'SS'),
            ('Gràcia', 'GR')
        )
    }


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
