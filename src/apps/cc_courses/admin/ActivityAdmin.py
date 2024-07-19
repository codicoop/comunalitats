from datetime import datetime

from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils import formats
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware
from django_summernote.admin import SummernoteModelAdminMixin
from constance import config
import modelclone

from apps.base.choices import ActivityFileType
from apps.coopolis.forms import ActivityForm, ActivityEnrolledForm
from apps.cc_courses.models import (
    Activity,
    ActivityEnrolled,
    ActivityResourceFile,
    ActivityFile,
)
from apps.coopolis.mixins import FilterByCurrentSubsidyPeriodMixin
from apps.cc_users.models import User
from apps.dataexports.models import SubsidyPeriod
from apps.facilities_reservations.models import Reservation


class FilterBySubsidyPeriod(admin.SimpleListFilter):
    """
    Allows Activities to be filtered according to their date_start using a
    dropdown with the subsidy periods.
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
            period = SubsidyPeriod.objects.get(id=value)
            return queryset.filter(date_start__range=(
                period.date_start, period.date_end)
            )
        return queryset


class FilterByJustificationFiles(admin.SimpleListFilter):
    """
    Allows Activities to be filtered by the existence of at least 1 internal
    file of the type "justification".
    """
    title = "Fitxer justificació"
    parameter_name = 'justification_file'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Sí'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            queryset = Activity.objects.filter(
                files__file_type=ActivityFileType.JUSTIFICATION,
            )
        if value == "No":
            queryset = Activity.objects.exclude(
                files__file_type=ActivityFileType.JUSTIFICATION,
            )
        return queryset


class ActivityEnrolledInline(admin.TabularInline):
    class Media:
        js = ('js/grappellihacks.js',)

    model = ActivityEnrolled
    form = ActivityEnrolledForm
    extra = 0
    fields = ['user', 'date_enrolled', 'waiting_list', 'user_comments',
              'send_enrollment_email', 'reminder_sent',
              'open_user_details_field', ]
    readonly_fields = (
        'date_enrolled', 'waiting_list', 'user_comments', 'reminder_sent',
        'open_user_details_field',
    )
    raw_id_fields = ('user',)
    autocomplete_lookup_fields = {
        'fk': ['user']
    }
    ordering = ["user__first_name", ]

    def open_user_details_field(self, obj):
        if obj.id is None:
            return '-'
        url = reverse(
            'admin:cc_users_user_change', kwargs={'object_id': obj.user.id})
        return format_html(
            f'<a href="{url}" target="_blank">Fitxa {obj.user.first_name}</a>')
    open_user_details_field.allow_tags = True
    open_user_details_field.short_description = 'Fitxa'


class ActivityResourcesInlineAdmin(admin.TabularInline):
    class Media:
        js = ('js/grappellihacks.js',)

    classes = ('grp-collapse', 'grp-closed')
    model = ActivityResourceFile
    extra = 0


class ActivityFileInlineAdmin(admin.TabularInline):
    class Media:
        js = ('js/grappellihacks.js',)

    classes = ('grp-collapse', 'grp-closed')
    model = ActivityFile
    extra = 0


class ActivityAdmin(FilterByCurrentSubsidyPeriodMixin, SummernoteModelAdminMixin, modelclone.ClonableModelAdmin):
    class Media:
        js = ('js/grappellihacks.js', 'js/chained_dropdown.js', )
        css = {
            'all': ('styles/grappellihacks.css',)
        }
    form = ActivityForm
    list_display = (
        'date_start', 'calculated_date_end', 'spots', 'remaining_spots', 'name',
        'service',
        'attendee_filter_field', 'attendee_list_field', 'send_reminder_field')
    readonly_fields = (
        'attendee_list_field', 'attendee_filter_field', 'send_reminder_field',
        'activity_poll_field', )
    summernote_fields = ('objectives', 'instructions',)
    search_fields = ('date_start', 'name', 'objectives',)
    list_filter = (
        FilterBySubsidyPeriod, FilterByJustificationFiles,
        "service", ("place__town", admin.RelatedOnlyFieldListFilter),
        'course', 'date_start', 'room', 'entities', 'place',
        'for_minors',
        ("responsible", admin.RelatedOnlyFieldListFilter),
    )
    fieldsets = [
        (None, {
            'fields': ['course', 'name', 'project_sector',  'types', 'description', 'objectives', 'place', 'room', 'date_start',
            'date_end', 'starting_time', 'ending_time', 'spots',
            'service', 'sub_service', 'communality_role', 'networking', 'agents_involved', 'neighborhood', 'estimated_hours', 'entities',
            'responsible', 'publish', 
            ]
        }),
        ("Documents per la justificació", {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('photo1', 'photo3', 'photo2', 'file1', ),
        }),
        ('Dades relatives a activitats per menors', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('for_minors', 'minors_school_name', 'minors_school_cif',
                       'minors_grade', 'minors_participants_number',
                       'minors_teacher'),
        }),
        ("Instruccions per les participants", {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('videocall_url', 'instructions'),
        }),
        ("Recursos i material formatiu", {
            # Grappelli way for sorting inlines
            'classes': ('placeholder resources-group',),
            'fields': (),
        }),
        ('Accions i llistats', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('attendee_list_field', 'attendee_filter_field',
                       'send_reminder_field', 'activity_poll_field', ),
        }),
        ("Fitxers interns", {
            'classes': ('placeholder files-group',),
            'fields': (),
        }),
    ]
    raw_id_fields = ('enrolled', 'course', 'entities',)
    autocomplete_lookup_fields = {
        'm2m': ['enrolled', 'entities'],
        'fk': ['course'],
    }
    date_hierarchy = 'date_start'
    inlines = (
        ActivityResourcesInlineAdmin,
        ActivityEnrolledInline,
        ActivityFileInlineAdmin,
    )
    subsidy_period_filter_param = 'subsidy_period'

    def get_form(self, request, obj=None, **kwargs):
        # Hack to be able to use self.request at the form.
        form = super(ActivityAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form

    def get_queryset(self, request):
        qs = super(ActivityAdmin, self).get_queryset(request)
        self.request = request
        return qs

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                r'<_id>/attendee-list/',
                self.admin_site.admin_view(self.attendee_list),
                name='attendee-list',
            ),
            path(
                r'<_id>/send-reminder/',
                self.admin_site.admin_view(self.send_reminder),
                name='send-activity-reminder'
            ),
            path(
                r'<_id>/send-poll/',
                self.admin_site.admin_view(self.send_poll),
                name='send-activity-poll'
            ),
        ]
        return custom_urls + urls

    def tweak_cloned_inline_fields(self, related_name, fields_list):
        """
        fields_list contains every m2m record that was in the Inline.

            Filtering for the "activityenrolled_set" just in case we add more
        inlines in the future.

        :param related_name: contains activityenrolled_set
        :param fields_list: contains [{'user': 897, 'user_comments': None},
        {'user': 898, 'user_comments': None}, ETC.
        :return: empty list
        """
        matches_name = related_name == "activityenrolled_set"
        return list() if matches_name else fields_list

    def render_change_form(self, request, context, *args, **kwargs):
        """ modelclone not showing Save button because of a bug.
        This workarounds it. """
        kwargs['add'] = True
        return super().render_change_form(request, context, *args, **kwargs)

    def remaining_spots(self, obj):
        return obj.remaining_spots

    remaining_spots.short_description = "Places disponibles"

    def attendee_list_field(self, obj):
        if obj.id is None:
            return '-'
        url = reverse_lazy('admin:attendee-list', kwargs={'_id': obj.id})
        return format_html(
            f'<a href="{url}" target="_new">Llista d\'assistencia</a>')

    attendee_list_field.allow_tags = True
    attendee_list_field.short_description = 'Exportar'

    @staticmethod
    def attendee_list(request, _id):
        import weasyprint
        import django.template.loader as loader
        temp = loader.get_template('admin/attendee_list.html')
        content = temp.render(
            {
                'assistants': Activity.objects.get(pk=_id).enrolled.filter(
                    enrollments__waiting_list=False),
                'activity': Activity.objects.get(pk=_id),
                'footer_image': config.ATTENDEE_LIST_FOOTER_IMG,
            }
        )

        pdf = weasyprint.HTML(
            string=content.encode('utf-8'),
            base_url=request.build_absolute_uri()
        )

        response = HttpResponse(
            pdf.write_pdf(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="llista_assistencia.pdf"'
        return response

    def attendee_filter_field(self, obj):
        if obj.id is None:
            return '-'
        base_url = reverse('admin:cc_users_user_changelist')
        return mark_safe(
            u'<a href="%s?enrolled_activities__exact=%d">Inscrites i '
            u'en llista d\'espera</a>' % (base_url, obj.id))

    attendee_filter_field.short_description = 'Llistat'

    def send_reminder_field(self, obj):
        if obj.id is None:
            return '-'
        url = reverse('admin:send-activity-reminder', kwargs={'_id': obj.id})
        return mark_safe(
            "<a href=\"{0}\">Enviar e-mails</a>".format(url))

    send_reminder_field.short_description = "Recordatori"

    def send_reminder(self, request, _id):
        # Confirmation page in admin inspired by:
        # https://gist.github.com/rsarai/d475c766871f40e52b8b4d1b12dedea2
        obj = Activity.objects.get(id=_id)
        if request.method == 'POST':
            if 'preview' in request.POST:
                mail = ActivityEnrolled.get_reminder_email(request.user, obj)
                mail.to = request.POST['preview_to']
                mail.send()
                self.message_user(
                    request,
                    "Correu de prova enviat correctament."
                )
                return HttpResponseRedirect(request.path_info)
            elif 'send' in request.POST or 'send_all' in request.POST:
                qs = obj.enrollments.filter(waiting_list=False)
                if 'send' in request.POST:
                    qs = qs.filter(reminder_sent__isnull=True)
                for enrollment in qs:
                    enrollment.send_reminder_email()
                self.message_user(
                    request,
                    "Recordatoris enviats correctament."
                )
                return HttpResponseRedirect("../../")

        context = {
            **self.admin_site.each_context(request),
            'obj': obj,
            'opts': self.model._meta,
        }
        return TemplateResponse(
            request, 'admin/reminder_confirmation.html', context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        if db_field.name == "minors_teacher":
            kwargs["queryset"] = User.objects.order_by("first_name", "last_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def activity_poll_field(self, obj):
        if obj.id is None:
            return '-'

        poll_status = "Oberta" if obj.poll_access_allowed() else "Tancada"
        results_url = reverse_lazy('admin:polls_activitypoll_changelist')
        text = "Accés als resultats (pestanya nova)"
        results_url = (f'<a href="{results_url}?activity__id__exact={obj.id}"'
                       f'target="_new">{text}</a>')
        poll_url = reverse('activity_poll', kwargs={'uuid': obj.uuid})
        poll_url = self.request.build_absolute_uri(poll_url)
        poll_url = f'<a href="{poll_url}" target="_blank">{poll_url}</a>'

        send_poll_url = reverse(
            'admin:send-activity-poll', kwargs={'_id': obj.id}
        )
        send_poll_url = self.request.build_absolute_uri(send_poll_url)
        send_poll_url = f'<a href="{send_poll_url}">Enviar enquesta</a>'
        poll_sent_date = formats.localize(obj.poll_sent) if obj.poll_sent else "Mai"
        poll_sent_text = f"Última data d'enviament de l'enquesta: {poll_sent_date}"

        content = (
            f"Estat: {poll_status}<br>"
            f"Enllaç: {poll_url}<br>"
            f"Resultats: {results_url}<br>"
            f"Enviament: {send_poll_url} ({poll_sent_text})"
        )
        return format_html(content)
    activity_poll_field.short_description = "Enquesta"

    def send_poll(self, request, _id):
        obj = Activity.objects.get(id=_id)
        if request.method == 'POST':
            if 'send' in request.POST or 'send_all' in request.POST:
                obj.send_poll_email()
                self.message_user(
                    request,
                    "Recordatoris enviats correctament."
                )
                return HttpResponseRedirect("../../")

        context = {
            **self.admin_site.each_context(request),
            'obj': obj,
            'opts': self.model._meta,
        }
        return TemplateResponse(
            request, 'admin/poll_sending.html', context)

    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        for obj in formset.cleaned_data:
            if (
                    'send_enrollment_email' in obj and
                    obj['send_enrollment_email'] is True
            ):
                if isinstance(obj['id'], ActivityEnrolled):
                    # Then la inscripció ja existeix i l'estan editant.
                    # Podem trobar l'objecte a instances:
                    obj = instances[instances.index(obj['id'])]
                else:
                    # Then és una nova inscripció a la que se li ha marcat
                    # l'enviament de notificació. No he trobat cap manera
                    # de connectar directament el que ve al cleaned_data
                    # amb l'objecte ja desat. Per tant cal fer query.
                    obj = obj['user'].enrollments.get(
                        activity=obj['activity']
                    )
                obj.send_confirmation_email()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.synchronize_with_reserved_room(obj, change)

    def synchronize_with_reserved_room(self, obj, change):
        # Si és una nova sessió i s'ha seleccionat self.room:
        # Si estem editant una sessió que no tenia una reserva, i ara sí que
        # n'ha de tenir:
        if (
            obj.room
            and (
                not change
                or (
                    change
                    and not obj.room_reservation
                    and obj.room
                )
            )
        ):
            reservation_obj = self.create_update_reservation(
                obj,
                obj.room_reservation,
            )
            obj.room_reservation = reservation_obj
            obj.save()

        # Si estem editant una sessió que ja tenia una reserva però han
        # deseleccionat la sala:
        if change and obj.room_reservation and not obj.room:
            if obj.room_reservation:
                self.delete_reservation(obj.room_reservation)

        # Si estem editant una sessió que ja tenia reserva i que n'ha de
        # continuar tenint:
        if change and obj.room_reservation and obj.room:
            reservation_obj = self.create_update_reservation(
                obj,
                obj.room_reservation,
            )
            obj.room_reservation = reservation_obj
            obj.save()

    def create_update_reservation(self, activity_obj, reservation_obj):
        date_end = activity_obj.date_start
        if activity_obj.date_end:
            date_end = activity_obj.date_end
        values = {
            "title": activity_obj.name,
            "start": make_aware(
                datetime.combine(
                    activity_obj.date_start,
                    activity_obj.starting_time,
                )
            ),
            "end": make_aware(
                datetime.combine(
                    date_end, activity_obj.ending_time,
                )
            ),
            "room": activity_obj.room,
            "responsible": self.request.user,
            "created_by": self.request.user,
        }
        reservation_obj, created = Reservation.objects.update_or_create(
            id=getattr(reservation_obj, "id", None),
            defaults=values,
        )
        return reservation_obj

    def delete_reservation(self, reservation_obj):
        reservation_obj.delete()
