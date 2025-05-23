from django.urls import reverse, reverse_lazy
from django.utils import formats
from django_object_actions import DjangoObjectActions
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from constance import config
from functools import update_wrapper
from django.conf.urls import url

from apps.coopolis.mixins import FilterByCurrentSubsidyPeriodMixin
from apps.cc_users.models import User
from apps.projects.models import Project, ProjectStage, EmploymentInsertion
from apps.projects.forms import ProjectFormAdmin, EmploymentInsertionForm, \
    ProjectStageFormAdmin
from apps.projects.models import ProjectStageSession, ProjectFile
from apps.dataexports.models import SubsidyPeriod
from conf.custom_mail_manager import MyMailTemplate


class FilterByFounded(admin.SimpleListFilter):
    """
    Deprecated in may 2024. Removed from ProjectAdmin's list_filter.
    If CIF and constitution_date are non empty.
    """
    title = 'Que tinguin CIF i Data de constitució'
    parameter_name = 'is_founded'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Sí'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(cif__isnull=False, constitution_date__isnull=False)
        return queryset


class ProjectStageSessionsInline(admin.StackedInline):
    model = ProjectStageSession
    extra = 0
    min_num = 0
    show_change_link = False
    can_delete = True
    empty_value_display = '(cap)'
    raw_id_fields = ('involved_partners',)
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }
    fields = (
        "session_responsible",
        "date",
        "hours",
        "follow_up",
        "entity",
        "involved_partners",
        "project_partners",
        "justification_file",
    )
    readonly_fields = ("project_partners", )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "session_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True).order_by("first_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FilterBySubsidyPeriod(admin.SimpleListFilter):
    """
    Allows Activities to be filtered according to their date_start using a
    dropdown with the subsidy periods.
    In ProjectStage, we're using this instead of just specifying the field in
    ProjectStageAdmin.list_filter because we wanted to skip the All option in
    the filter, for consistency with the FilterByCurrentSubsidyPeriodMixin
    behaviour.
    """
    title = "Convocatòria"
    parameter_name = 'subsidy_period'

    def lookups(self, request, model_admin):
        qs = SubsidyPeriod.objects.all()
        qs.order_by('name')
        return list(qs.values_list('id', 'name'))

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(subsidy_period_id=value)
        return queryset

    def choices(self, changelist):
        choices = super().choices(changelist)
        choices.__next__()
        for choice in choices:
            yield choice


class ProjectStageAdmin(FilterByCurrentSubsidyPeriodMixin, admin.ModelAdmin):
    form = ProjectStageFormAdmin
    empty_value_display = '(cap)'
    list_display = (
        'project_field_ellipsis', 'date_start', 'stage_type',
        'responsible_field_ellipsis',
        'service', 'subsidy_period', '_has_certificate',
        '_participants_count', 'project_field', 'justification_documents_total',
    )
    list_filter = (
        FilterBySubsidyPeriod, 'service',
        ('responsible', admin.RelatedOnlyFieldListFilter),
        'date_start', 'stage_type',
        'project__sector'
    )
    actions = ["export_as_csv"]
    search_fields = ['project__name__unaccent']
    fieldsets = [
        (None, {
            'fields': [
                'course', 'project', 'project_sector', 'stage_type', 'types',
                'subsidy_period', 'service', 
                'sub_service', 'communality_role', 'networking', 'agents_involved', 'responsible', 'scanned_certificate',
                'hours_sum', 'date_start',
                "earliest_session_field",
                "justification_documents_total",
            ]
        }),
        ("Sessions d'acompanyament", {
            # Grappelli way for sorting inlines
            'classes': ('placeholder stage_sessions-group',),
            'fields': (),
        }),
    ]
    inlines = (ProjectStageSessionsInline, )
    readonly_fields = (
        'hours_sum',
        "earliest_session_field",
        "justification_documents_total",
    )
    subsidy_period_filter_param = "subsidy_period"
    raw_id_fields = ('course', )
    autocomplete_lookup_fields = {
        'fk': ['course'],
    }

    class Media:
        js = ('js/grappellihacks.js', 'js/chained_dropdown.js', )
        css = {
            'all': ('styles/grappellihacks.css',)
        }

    def _has_certificate(self, obj):
        if obj.scanned_certificate:
            v = (f"<a href=\"{obj.scanned_certificate.url}\" "
                 f"target=\"_blank\"><img "
                 f"src=\"/static/admin/img/icon-yes.svg\" alt=\"True\"></a>")
            return mark_safe(v)
        return mark_safe(
            "<img src=\"/static/admin/img/icon-no.svg\" alt=\"True\">"
        )
    _has_certificate.short_description = "Certificat"

    def _participants_count(self, obj):
        return obj.involved_partners_count
    _participants_count.short_description = "Participants"

    def project_field_ellipsis(self, obj):
        if len(obj.project.name) > 50:
            return "%s..." % obj.project.name[:50]
        return obj.project.name
    project_field_ellipsis.short_description = "Fitxa"

    def responsible_field_ellipsis(self, obj):
        if obj.responsible and len(str(obj.responsible)) > 15:
            return "%s..." % str(obj.responsible)[:15]
        return obj.responsible
    responsible_field_ellipsis.short_description = 'Responsable'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True).order_by("first_name")
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def project_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s/%d/change">%s</a>' % (
            'coopolis', 'project', obj.project.id, 'Veure'))
    project_field.short_description = 'Projecte'

    def earliest_session_field(self, obj):
        try:
            session = obj.stage_sessions.earliest("date")
        except obj.DoesNotExist:
            return "No hi ha cap sessió d'acompanyament."
        return formats.localize(session.date)
    earliest_session_field.short_description = 'Primera sessió'


class ProjectStagesInline(admin.StackedInline):
    model = ProjectStage
    extra = 0
    min_num = 0
    show_change_link = True
    can_delete = False
    empty_value_display = '(cap)'
    fieldsets = (
        (None, {
            'fields': [
                "stage_sessions_field",
                'project',
                'stage_type',
                'subsidy_period',
                'service',
                'sub_service',
                'responsible',
                'scanned_certificate',
                'hours_sum',
                'date_start',
                "earliest_session_field",
                "justification_documents_total",
            ]
        }),
    )
    readonly_fields = (
        'stage_type',
        'subsidy_period',
        'service',
        'sub_service',
        'responsible',
        'scanned_certificate',
        'hours_sum',
        'date_start',
        'stage_sessions_field',
        "earliest_session_field",
        "justification_documents_total",
    )
    class Media:
        js = ('js/chained_dropdown.js', )
        
    def stage_sessions_field(self, obj):
        if not obj.id:
            url = reverse_lazy('admin:projects_projectstage_add')
            url = (f'Per crear un acompanyament <a href="{url}'
            f'#stage_sessions-group"> clica aquí</a>.')
            return mark_safe(url)
        count = obj.sessions_count()
        url = reverse_lazy(
            'admin:projects_projectstage_change',
            kwargs={'object_id': obj.id}
        )
        url = (f'<a href="{url}#stage_sessions-group">Anar a la fitxa de la '
               f'Justificació (per veure i editar les sessions)</a>')
        txt = f"{count} - {url}"
        return mark_safe(txt)

    stage_sessions_field.short_description = "Sessions d'acompanyament"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True).order_by("first_name")
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def earliest_session_field(self, obj):
        try:
            session = obj.stage_sessions.earliest("date")
        except obj.DoesNotExist:
            return "No hi ha cap sessió d'acompanyament."
        return formats.localize(session.date)
    earliest_session_field.short_description = 'Primera sessió'


class ProjectFileInline(admin.TabularInline):
    class Media:
        js = ('js/grappellihacks.js',)

    classes = ('grp-collapse', 'grp-closed')
    model = ProjectFile
    extra = 0


class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_field',)

    def project_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s/%d/change">%s</a>' % (
            'coopolis', 'project', obj.project.id, obj.project.name))
    project_field.short_description = 'Projecte'

    def has_add_permission(self, request, obj=None):
        return False


class ProjectAdmin(DjangoObjectActions, admin.ModelAdmin):
    class Media:
        js = ('js/grappellihacks.js',)
        css = {
            'all': ('styles/grappellihacks.css',)
        }

    form = ProjectFormAdmin
    list_display = (
        'name', 'mail', 'phone', 'registration_date', 'constitution_date',
        'stages_field', 'last_stage_responsible',
    )
    search_fields = (
        'id', 'name__unaccent', 'web', 'mail', 'phone', 'registration_date', 'project_origins', 'social_base', 'sector'
    )
    list_filter = ('registration_date', 'sector', 'project_status', 'tags', )
    fieldsets = (
        ("Dades generals", {
            'fields': ['name', 'sector', 'web', 'project_status', 'motivation',
                       'mail', 'phone', 'entity_name', 'cif', 'entity_type',
                       'project_sector', 'town', 'neighborhood', 'annuity',
                       'number_people',
                       'project_origins', 'social_base']
        }),
        ("Dades internes gestionades per la comunalitat", {
            'fields': ['partners', 'partners_participants',
                       'registration_date', 'constitution_date', 'description',
                       'employment_estimation', 'other', 'follow_up_situation',
                       'follow_up_situation_update', 'tags']
        }),
        ("Activitats a les que s'han inscrit sòcies del projecte", {
            'fields': ['partners_activities', ]
        })
    )
    readonly_fields = (
        'id', 'follow_up_situation_update', 'partners_activities',
        'partners_participants',
    )
    actions = ["export_as_csv"]
    change_actions = ('print', )
    print_template = 'admin/my_test/myentry/review.html'
    inlines = (ProjectFileInline, ProjectStagesInline, )
    raw_id_fields = ('partners',)
    autocomplete_lookup_fields = {
        'm2m': ['partners'],
    }

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [
            url(r'(?P<id>\d+)/print/$', wrap(self.print),
                name='%s_%s_print' % info),
        ]

        return my_urls + urls

    def print(self, request, obj):
        # Confirmation page in admin inspired by: https://gist.github.com/rsarai/d475c766871f40e52b8b4d1b12dedea2
        from django.template.response import TemplateResponse

        context = {
            **self.admin_site.each_context(request),
            'obj': obj,
            'opts': self.model._meta,
        }
        return TemplateResponse(
            request, 'admin/project_print.html', context)

    print.label = "Imprimir"
    print.short_description = "Visualitza la fitxa en un format imprimible"
    print.attrs = {
        'target': '_blank',
    }

    def stages_field(self, obj):
        if obj.stages_list:
            return mark_safe(
                f"<a href=\"../../coopolis/projectstage?project__exact"
                f"={ obj.id }\">{ obj.stages_list }</a>")
        return None

    stages_field.short_description = 'Acompanyaments'


class DerivationAdmin(admin.ModelAdmin):
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


class EmploymentInsertionAdmin(admin.ModelAdmin):
    model = EmploymentInsertion
    form = EmploymentInsertionForm
    list_display = ('insertion_date', 'activity', 'user', 'contract_type', 'subsidy_period', )
    list_filter = ('subsidy_period', 'contract_type', 'insertion_date',)
    search_fields = ('activity__name__unaccent', 'user__first_name__unaccent', )
    raw_id_fields = ('user', 'activity',)
    autocomplete_lookup_fields = {
        'fk': ['user', 'activity', ],
    }


class StageSubtypeAdmin(admin.ModelAdmin):
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


@admin.register(ProjectStageSession)
class ProjectStageSessionAdmin(FilterByCurrentSubsidyPeriodMixin, admin.ModelAdmin):
    empty_value_display = '(cap)'
    raw_id_fields = ('involved_partners',)
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }
    fields = (
        "project_stage",
        "session_responsible",
        "date",
        "hours",
        "follow_up",
        "entity",
        "involved_partners",
        "project_partners",
        "justification_file",
    )
    readonly_fields = (
        "project_partners",
        "project_field",
        "stage_type_field",
        "stage_responsible_field",
    )
    list_display = (
        "date",
        "project_field",
        "stage_type_field",
        "hours",
        "session_responsible",
        "stage_responsible_field",
        "entity",
        "justification_file",
    )
    list_filter = (
        ("project_stage__subsidy_period", admin.RelatedOnlyFieldListFilter),
        ("session_responsible", admin.RelatedOnlyFieldListFilter),
    )
    subsidy_period_filter_param = "project_stage__subsidy_period__id__exact"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "session_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True).order_by("first_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def project_field(self, obj):
        if obj.project_stage.project:
            url = reverse(
                "admin:projects_project_change",
                kwargs={'object_id': obj.project_stage.project.id}
            )
            return mark_safe(f'<a href="{ url }">{ obj.project_stage.project }</a>')
        return None
    project_field.short_description = 'Projecte'

    def stage_type_field(self, obj):
        if obj:
            return obj.project_stage.get_stage_type_display()
        return None
    stage_type_field.short_description = 'Tipus'

    def stage_responsible_field(self, obj):
        if obj:
            return obj.project_stage.responsible
        return None
    stage_responsible_field.short_description = 'Responsable'
