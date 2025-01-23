from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from apps.coopolis.mixins import FilterByCurrentSubsidyPeriodMixin
from apps.dataexports.models import DataExports, SubsidyPeriod


@admin.register(SubsidyPeriod)
class SubsidyPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'date_start', 'date_end')
    readonly_fields = ('name',)

@admin.register(DataExports)
class DataExportsAdmin(FilterByCurrentSubsidyPeriodMixin, admin.ModelAdmin):
    list_display = ('name', 'subsidy_period', 'export_data_field',)
    readonly_fields = ('created',)
    list_filter = (("subsidy_period", admin.RelatedOnlyFieldListFilter), )
    subsidy_period_filter_param = "subsidy_period__id__exact"

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
        from apps.dataexports.export_functions import ExportFunctions
        obj = DataExports.objects.get(id=_id)
        instance = ExportFunctions()
        return instance.callmethod(obj)
