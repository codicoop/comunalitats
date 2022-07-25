from django.http import HttpResponseNotFound

from apps.dataexports.exports.justification import ExportJustification
from apps.dataexports.exports.justification_service import \
    ExportJustificationService
from apps.dataexports.exports.polls import ExportPolls, ExportPollsByServices


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

    def export(self, export_obj):
        controller = ExportJustification(export_obj)
        return controller.export()

    def export_service(self, export_obj):
        controller = ExportJustificationService(export_obj)
        return controller.export()

    def export_polls(self, export_obj):
        controller = ExportPolls(export_obj)
        return controller.export()

    def export_polls_by_services(self, export_obj):
        controller = ExportPollsByServices(export_obj)
        return controller.export()
