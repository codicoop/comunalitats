from django.urls import reverse
from django_object_actions import DjangoObjectActions
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from constance import config
from functools import update_wrapper
from django.conf.urls import url

from coopolis.models import User, Project, ProjectStage, EmploymentInsertion, StagesByAxis
from coopolis.forms import ProjectFormAdmin, ProjectStageInlineForm, ProjectStageForm
from coopolis_backoffice.custom_mail_manager import MyMailTemplate


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


class ProjectStageAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/grappellihacks.js',)
        css = {
            'all': ('styles/grappellihacks.css',)
        }

    form = ProjectStageForm
    empty_value_display = '(cap)'
    list_display = ('project_field_ellipsis', 'date_start', 'stage_responsible_field_ellipsis', 'stage_type',
                    'axis_summary', 'entity', 'subsidy_period', 'project_field')
    list_filter = ('subsidy_period', ('stage_responsible', admin.RelatedOnlyFieldListFilter), 'date_start',
                   'stage_type', 'axis', 'entity', 'project__sector')
    actions = ["export_as_csv"]
    search_fields = ['project__name__unaccent']
    raw_id_fields = ('involved_partners',)
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }
    fieldsets = [
        (None, {
            'fields': ['project', 'stage_type', 'subsidy_period', 'date_start',
                       'date_end', 'follow_up', 'axis', 'subaxis', 'entity',
                       'stage_organizer', 'stage_responsible',
                       'scanned_signatures', 'scanned_certificate', 'hours',
                       'involved_partners', ]
        })
    ]

    def project_field_ellipsis(self, obj):
        if len(obj.project.name) > 50:
            return "%s..." % obj.project.name[:50]
        return obj.project.name

    def stage_responsible_field_ellipsis(self, obj):
        if obj.stage_responsible and len(str(obj.stage_responsible)) > 15:
            return "%s..." % str(obj.stage_responsible)[:15]
        return obj.stage_responsible
    stage_responsible_field_ellipsis.short_description = 'Responsable'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "stage_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def project_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s/%d/change">%s</a>' % (
            'coopolis', 'project', obj.project.id, 'Veure'))
    project_field.short_description = 'Projecte'

    def get_fieldsets(self, request, obj=None):
        """
        For ateneus enabling cofunded options: Adding the Cofinançades fieldset.
        """
        fs = ('Opcions de cofinançament', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('cofunded', 'cofunded_ateneu', 'strategic_line',),
        })
        if config.ENABLE_COFUNDED_OPTIONS and fs not in self.fieldsets:
            self.fieldsets.insert(1, fs)

        return self.fieldsets


class ProjectStagesInline(admin.StackedInline):
    model = ProjectStage
    form = ProjectStageInlineForm
    extra = 0
    min_num = 0
    show_change_link = True
    can_delete = False
    empty_value_display = '(cap)'

    raw_id_fields = ('involved_partners',)
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "stage_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EmploymentInsertionInline(admin.TabularInline):
    class Media:
        js = ('js/grappellihacks.js',)

    model = EmploymentInsertion
    extra = 0
    raw_id_fields = ('user',)
    autocomplete_lookup_fields = {
        'fk': ['user']
    }


class ProjectAdmin(DjangoObjectActions, admin.ModelAdmin):
    class Media:
        js = ('js/grappellihacks.js',)
        css = {
            'all': ('styles/grappellihacks.css',)
        }

    form = ProjectFormAdmin
    list_display = ('id', 'name', 'mail', 'phone', 'registration_date', 'constitution_date', 'stages_field',
                    'last_stage_responsible',)
    search_fields = ('id', 'name__unaccent', 'web', 'mail', 'phone', 'registration_date',
                     'object_finality', 'project_origins', 'solves_necessities', 'social_base', 'sector')
    list_filter = ('registration_date', 'sector', 'project_status',
                   FilterByFounded, 'tags', )
    fieldsets = (
        ("Dades que s'omplen des de la web", {
            'fields': ['name', 'sector', 'web', 'project_status', 'motivation', 'mail', 'phone', 'town', 'district',
                       'number_people', 'estatuts', 'viability', 'sostenibility', 'object_finality', 'project_origins',
                       'solves_necessities', 'social_base']
        }),
        ("Dades internes gestionades per l'ateneu", {
            'fields': ['partners', 'registration_date', 'cif', 'constitution_date', 'subsidy_period', 'derivation',
                       'derivation_date', 'description', 'employment_estimation', 'other', 'follow_up_situation',
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
    inlines = (ProjectStagesInline, EmploymentInsertionInline,)
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
            url(r'(?P<id>\d+)/print/$', wrap(self.print), name='%s_%s_print' % info),
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
                f"<a href=\"../../coopolis/projectstage?project__exact={ obj.id }\">{ obj.stages_list }</a>")
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

                new_partners_list = post_partners_list.difference(current_partners_list)
            else:
                new_partners_list = post_partners_list

            new_partner_objects = User.objects.filter(pk__in=new_partners_list)
            for new_partner in new_partner_objects:
                self.send_added_to_project_email(new_partner.email, request.POST['name'])

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
            'url_projectes': f"{settings.ABSOLUTE_URL}{reverse('project_info')}",
            'url_backoffice': settings.ABSOLUTE_URL
        }
        mail.send()


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
    list_display = ('insertion_date', 'project', 'user', 'contract_type', 'duration', 'subsidy_period',)
    list_filter = ('subsidy_period', 'contract_type', 'insertion_date', )
    search_fields = ('project__name__unaccent', 'user__first_name__unaccent', )
    raw_id_fields = ('user', 'project',)
    autocomplete_lookup_fields = {
        'fk': ['user', 'project', ],
    }


class ProjectStageAdminAxis(admin.ModelAdmin):
    class Media:
        js = ('js/grappellihacks.js',)
        css = {
            'all': ('styles/grappellihacks.css',)
        }

    empty_value_display = '(cap)'
    list_display = ('axis_summary', 'entity', 'date_start', 'project_field_ellipsis',
                    'stage_responsible_field_ellipsis', 'stage_type', 'subsidy_period', 'project_field')
    list_filter = ('subsidy_period', ('stage_responsible', admin.RelatedOnlyFieldListFilter), 'date_start',
                   'stage_type', 'axis', 'entity', 'project__sector')
    actions = ["export_as_csv"]
    search_fields = ['project__name__unaccent']

    def project_field_ellipsis(self, obj):
        if len(obj.project.name) > 50:
            return "%s..." % obj.project.name[:50]
        return obj.project.name

    def stage_responsible_field_ellipsis(self, obj):
        if obj.stage_responsible and len(str(obj.stage_responsible)) > 15:
            return "%s..." % str(obj.stage_responsible)[:15]
        return obj.stage_responsible
    stage_responsible_field_ellipsis.short_description = 'Responsable'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "stage_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def project_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s/%d/change">%s</a>' % (
            'coopolis', 'project', obj.project.id, 'Veure'))

    project_field.short_description = 'Projecte'

    raw_id_fields = ('involved_partners',)
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }
