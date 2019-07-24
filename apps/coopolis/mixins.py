import csv
from django.http import HttpResponse


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
