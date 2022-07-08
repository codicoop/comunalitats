import csv
from django.http import HttpResponse, HttpResponseRedirect

from apps.coopolis.exceptions import MissingCurrentSubsidyPeriod
from apps.dataexports.models import SubsidyPeriod


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar la selecció a CSV"


class FormDistrictValidationMixin:
    def clean(self):
        cleaned_data = super().clean()
        town = cleaned_data.get("town")
        district = cleaned_data.get("district")

        if str(town) == "BARCELONA" and district is None:
            msg = "Si la població és Barcelona, cal seleccionis un districte."
            self.add_error('district', msg)


class FilterByCurrentSubsidyPeriodMixin:
    """
    Mixin for admin.ModelAdmin

    The subsidy_period_filter_param needs to be filled with the GET param name that filters the subsidy period.
    An easy way to obtain it is:
    1. Use the filter in admin to chagne to another period.
    2. Look at the query params and copy the subsidy period one.

    I.e: subsidy_period_filter_param = "stages__subsidy_period__id__exact"
    """
    subsidy_period_filter_param = None

    def changelist_view(self, request, extra_context=None):
        if self.subsidy_period_filter_param and self.subsidy_period_filter_param not in request.GET:
            return self.redirect_to_current_period(request)
        return super().changelist_view(request, extra_context)

    def redirect_to_current_period(self, request):
        current = SubsidyPeriod.get_current()
        if current:
            value = str(current.id)
        else:
            raise MissingCurrentSubsidyPeriod(
                "El llistat per defecte es carrega mostrant la convocatòria "
                "vigent, però ha fallat a l'intentar-la trobar. Si us plau "
                "revisa que existeixi una convocatòria creada per la data "
                "actual."
            )
        query_string = request.META['QUERY_STRING']
        value = f"{self.subsidy_period_filter_param}={value}"
        if query_string != '':
            value = f"&{value}"
        query_string = query_string + value
        return HttpResponseRedirect(f"{request.path_info}?{query_string}")
