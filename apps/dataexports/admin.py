from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from dataexports.models import DataExports


@admin.register(DataExports)
class DataExportsAdmin(admin.ModelAdmin):
    list_display = ('name', 'subsidy_period', 'export_data_field',)
    readonly_fields = ('created',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                r'<_id>/export-data/',
                self.admin_site.admin_view(self.export_data),
                name='export-data',
            ),
        ]
        return custom_urls + urls

    def export_data_field(self, obj):
        if obj.id is None:
            return '-'
        return format_html(
            '<a href="%s" target="_new">Excel</a>' % reverse('admin:export-data', kwargs={'_id': obj.id}))

    export_data_field.short_description = 'Exportar'

    def export_data(self, request, _id):
        from dataexports.export_functions import ExportFunctions
        obj = DataExports.objects.get(id=_id)
        instance = ExportFunctions()
        return instance.callmethod(obj.function_name)
