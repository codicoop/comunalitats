from django.urls import reverse, reverse_lazy
from django.utils import formats
from django_object_actions import DjangoObjectActions
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from constance import config
from functools import update_wrapper
from django.conf.urls import url

from apps.coopolis.models import User, Project, ProjectStage, EmploymentInsertion
from apps.coopolis.forms import (
    ProjectFormAdmin,
    EmploymentInsertionInlineFormSet,
)
from apps.coopolis.models.projects import ProjectStageSession, ProjectFile
from conf.custom_mail_manager import MyMailTemplate


class FilterByFounded(admin.SimpleListFilter):
    """
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "session_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True).order_by("first_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProjectStageAdmin(admin.ModelAdmin):
    empty_value_display = '(cap)'
    list_display = (
        'project_field_ellipsis', 'date_start', 'stage_type',
        'stage_responsible_field_ellipsis',
        'axis_summary', 'subsidy_period', '_has_certificate',
        '_participants_count', 'project_field'
    )
    list_filter = (
        'subsidy_period',
        'service',
        ('stage_responsible', admin.RelatedOnlyFieldListFilter),
        'date_start', 'stage_type', 'axis',
        'circle', 'project__sector'
    )
    actions = ["export_as_csv"]
    search_fields = ['project__name__unaccent']
    raw_id_fields = ('involved_partners',)
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }
    fieldsets = [
        (None, {
            'fields': ['project', 'stage_type',
                       'subsidy_period', 'service',
                       'circle', 'stage_responsible',
                       'scanned_certificate',
                       'involved_partners', 'hours_sum', 'date_start',
                       "earliest_session_field", ]
        }),
        ("Camps convocatòries < 2020", {
            'fields': ["axis", "subaxis", ]
        }),
    ]
    inlines = (ProjectStageSessionsInline, )
    readonly_fields = ('hours_sum', 'date_start', "earliest_session_field", )

    class Media:
        js = ('js/grappellihacks.js',)
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
        return len(obj.involved_partners.all())
    _participants_count.short_description = "Participants"

    def project_field_ellipsis(self, obj):
        if len(obj.project.name) > 50:
            return "%s..." % obj.project.name[:50]
        return obj.project.name
    project_field_ellipsis.short_description = "Fitxa"

    def stage_responsible_field_ellipsis(self, obj):
        if obj.stage_responsible and len(str(obj.stage_responsible)) > 15:
            return "%s..." % str(obj.stage_responsible)[:15]
        return obj.stage_responsible
    stage_responsible_field_ellipsis.short_description = 'Responsable'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "stage_responsible":
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

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        # For ateneus enabling cofunded options: Adding the Cofinançades
        # fieldset.
        fs = ('Opcions de cofinançament', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('cofunded', 'cofunded_ateneu', 'strategic_line',),
        })
        if config.ENABLE_COFUNDED_OPTIONS and fs not in self.fieldsets:
            fieldsets.insert(1, fs)

        # For ateneus enabling stage_subtype: Adding the Subtype field.
        if config.ENABLE_STAGE_SUBTYPES is True:
            fieldsets[0][1]['fields'] = self.get_fields_with_type(
                fieldsets[0][1]['fields']
            )

        return fieldsets

    def get_fields(self, request, obj=None):
        return self.get_fields_with_type(super().get_fields(request, obj))

    def get_list_display(self, request):
        return self.get_fields_with_type(super().get_list_display(request))

    def get_list_filter(self, request):
        return self.get_fields_with_type(super().get_list_filter(request))

    @staticmethod
    def get_fields_with_type(fields):
        fields = list(fields)
        if (
            config.ENABLE_STAGE_SUBTYPES is True
            and 'stage_subtype' not in fields
        ):
            type_index = 0
            if 'stage_type' in fields:
                type_index = fields.index('stage_type') + 1
            fields.insert(type_index, 'stage_subtype')
        return fields


class ProjectStagesInline(admin.StackedInline):
    model = ProjectStage
    extra = 0
    min_num = 0
    show_change_link = True
    can_delete = False
    empty_value_display = '(cap)'
    raw_id_fields = ('involved_partners',)
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }
    fieldsets = (
        (None, {
            'fields': ['project', 'stage_type',
                       'subsidy_period', 'service',
                       'circle', 'stage_responsible',
                       'scanned_certificate',
                       'involved_partners', 'hours_sum', 'date_start',
                       "earliest_session_field", "stage_sessions_field", ]
        }),
        ("Camps convocatòries < 2020", {
            'fields': ["axis", "subaxis", ]
        }),
    )
    readonly_fields = ('hours_sum', 'date_start', 'stage_sessions_field',
                       "earliest_session_field",)

    def stage_sessions_field(self, obj):
        count = obj.sessions_count()
        url = reverse_lazy(
            'admin:coopolis_projectstage_change',
            kwargs={'object_id': obj.id}
        )
        url = (f'<a href="{url}#stage_sessions-group">Anar a la fitxa de la '
               f'Justificació (per veure i editar les sessions)</a>')
        txt = f"{count} - {url}"
        return mark_safe(txt)

    stage_sessions_field.short_description = "Sessions d'acompanyament"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "stage_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
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

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        # For ateneus enabling stage_subtype: Adding the Subtype field.
        if config.ENABLE_STAGE_SUBTYPES is True:
            fieldsets[0][1]['fields'] = ProjectStageAdmin.get_fields_with_type(
                fieldsets[0][1]['fields']
            )

        return fieldsets


class EmploymentInsertionInline(admin.TabularInline):
    class Media:
        js = ('js/grappellihacks.js',)

    model = EmploymentInsertion
    formset = EmploymentInsertionInlineFormSet
    extra = 0
    raw_id_fields = ('user',)
    autocomplete_lookup_fields = {
        'fk': ['user']
    }


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
        'id', 'name', 'mail', 'phone', 'registration_date',
        'constitution_date', 'stages_field', 'last_stage_responsible',
        '_insertions_count'
    )
    search_fields = (
        'id', 'name__unaccent', 'web', 'mail', 'phone', 'registration_date',
        'object_finality', 'project_origins', 'solves_necessities',
        'social_base', 'sector'
    )
    list_filter = ('registration_date', 'sector', 'project_status',
                   FilterByFounded, 'tags', )
    fieldsets = (
        ("Dades que s'omplen des de la web", {
            'fields': ['name', 'sector', 'web', 'project_status', 'motivation',
                       'mail', 'phone', 'town', 'district', 'number_people',
                       'estatuts', 'viability', 'sostenibility',
                       'object_finality', 'project_origins',
                       'solves_necessities', 'social_base']
        }),
        ("Dades internes gestionades per l'ateneu", {
            'fields': ['partners', 'registration_date', 'cif',
                       'constitution_date', 'subsidy_period', 'derivation',
                       'derivation_date', 'description',
                       'employment_estimation', 'other', 'follow_up_situation',
                       'follow_up_situation_update', 'tags']
        }),
        ("Activitats a les que s'han inscrit sòcies del projecte", {
            'fields': ['partners_activities', ]
        })
    )
    readonly_fields = (
        'id', 'follow_up_situation_update', 'partners_activities',
    )
    actions = ["export_as_csv"]
    change_actions = ('print', )
    print_template = 'admin/my_test/myentry/review.html'
    inlines = (ProjectFileInline, ProjectStagesInline,
               EmploymentInsertionInline,)
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

    def save_model(self, request, obj, form, change):
        if request.POST['partners']:
            """ Sending a notification e-mail to newly added partners. """

            # request.POST['partners'] is a string: '1594,98'
            # Transforming it to a list:
            post_partners_list = request.POST['partners'].split(',')
            post_partners_list = [int(i) for i in post_partners_list]
            post_partners_list = set(sorted(post_partners_list))

            # Determine which are the newly added partners depending on editing or creating project.
            if change:
                current_partners = obj.partners.all()
                current_partners_list = set()
                for partner in current_partners:
                    current_partners_list.add(partner.pk)
                current_partners_list = set(sorted(current_partners_list))

                new_partners_list = post_partners_list.difference(
                    current_partners_list)
            else:
                new_partners_list = post_partners_list

            new_partner_objects = User.objects.filter(pk__in=new_partners_list)
            for new_partner in new_partner_objects:
                self.send_added_to_project_email(new_partner.email,
                                                 request.POST['name'])

        super().save_model(request, obj, form, change)

    def send_added_to_project_email(self, mail_to, project_name):
        mail = MyMailTemplate('EMAIL_ADDED_TO_PROJECT')
        mail.to = mail_to
        mail.subject_strings = {
            'projecte_nom': project_name
        }
        mail.body_strings = {
            'ateneu_nom': config.PROJECT_FULL_NAME,
            'projecte_nom': project_name,
            'url_projectes': settings.ABSOLUTE_URL + reverse('project_info'),
            'url_backoffice': settings.ABSOLUTE_URL
        }
        mail.send()

    def _insertions_count(self, obj):
        if obj.employment_insertions:
            return len(obj.employment_insertions.all())
        return 0
    _insertions_count.short_description = "Insercions"


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
    list_display = ('insertion_date', 'project', 'user', 'contract_type',
                    'subsidy_period', 'circle', )
    list_filter = (
        'subsidy_period', 'contract_type', 'circle', 'insertion_date',
    )
    search_fields = ('project__name__unaccent', 'user__first_name__unaccent', )
    raw_id_fields = ('user', 'project',)
    autocomplete_lookup_fields = {
        'fk': ['user', 'project', ],
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
