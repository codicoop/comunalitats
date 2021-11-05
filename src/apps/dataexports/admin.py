from django.conf import settings
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from apps.dataexports.models import DataExports, SubsidyPeriod


@admin.register(SubsidyPeriod)
class SubsidyPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'date_start', 'date_end')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


@admin.register(DataExports)
class DataExportsAdmin(admin.ModelAdmin):
    list_display = ('name', 'subsidy_period', 'export_data_field',)
    readonly_fields = ('created',)
    list_filter = (("subsidy_period", admin.RelatedOnlyFieldListFilter), )

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

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and settings.DEBUG:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and settings.DEBUG:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser and settings.DEBUG:
            return True
        return False
