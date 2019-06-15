from coopolis.models import Project, ProjectStage, User
from cc_courses.models import Course, Activity
from django.http import HttpResponseNotFound


class ExportFunctions:

    @staticmethod
    def callmethod(name):
        if hasattr(ExportFunctions, name):
            getattr(ExportFunctions, name)()
        return HttpResponseNotFound("La funció especificada no existeix")

    @staticmethod
    def export_test():
        print("executed!")
