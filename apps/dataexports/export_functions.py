from django.http import HttpResponseNotFound

from dataexports.exports.cofunded import ExportJustificationCofunded
from dataexports.exports.covid_hours import ExportCovidHours
from dataexports.exports.justification import ExportJustification
from dataexports.exports.justification_2_itineraris import (
    ExportJustification2Itineraris
)
from dataexports.exports.memory import ExportMemory


class ExportFunctions:
    """
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
    def callmethod(self, obj):
        if hasattr(self, obj.function_name):
            return getattr(self, obj.function_name)(obj)
        else:
            message = "<h1>La funció especificada no existeix</h1>"
            return HttpResponseNotFound(message)

    def export_stages_descriptions(self, export_obj):
        controller = ExportMemory(export_obj)
        return controller.export_stages_descriptions()

    def export(self, export_obj):
        controller = ExportJustification(export_obj)
        return controller.export()

    def export_dos_itineraris(self, export_obj):
        controller = ExportJustification2Itineraris(export_obj)
        return controller.export_dos_itineraris()

    def export_cofunded(self, export_obj):
        controller = ExportJustificationCofunded(export_obj)
        return controller.export()

    def export_covid_hours(self, export_obj):
        controller = ExportCovidHours(export_obj)
        return controller.export()
