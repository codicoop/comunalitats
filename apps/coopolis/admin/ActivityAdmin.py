#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdminMixin
from constance import config
from django.conf import settings
import modelclone
from django.template import Template, Context

from coopolis.forms import ActivityForm
from cc_courses.models import Activity


class ActivityAdmin(SummernoteModelAdminMixin, modelclone.ClonableModelAdmin):
    form = ActivityForm
    list_display = ('date_start', 'spots', 'remaining_spots', 'name', 'attendee_filter_field', 'attendee_list_field',
                    'send_reminder_field')
    readonly_fields = ('attendee_list_field', 'attendee_filter_field', 'send_reminder_field')
    summernote_fields = ('objectives',)
    search_fields = ('date_start', 'name', 'objectives',)
    list_filter = ('course', 'date_start', 'justification', 'entity', 'axis', 'place', 'for_minors',)
    fieldsets = (
        (None, {
            'fields': ('course', 'name', 'objectives', 'place', 'date_start', 'date_end', 'starting_time',
                       'ending_time', 'spots', 'enrolled', 'axis', 'subaxis', 'entity', 'organizer')
        }),
        ('Dades relatives a activitats per menors', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('for_minors', 'minors_school_name', 'minors_school_cif', 'minors_grade', 'minors_participants_number',
                       'minors_teacher'),
        }),
        ('Accions i llistats', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('attendee_list_field', 'attendee_filter_field', 'send_reminder_field'),
        })
    )
    # define the raw_id_fields
    raw_id_fields = ('enrolled',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'm2m': ['enrolled'],
    }

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
        ]
        return custom_urls + urls

    def tweak_cloned_fields(self, fields):
        """ From ClonableModelAdmin. When cloning an Activity, we discard the enrolled people. """
        fields['enrolled'] = None
        return fields

    def render_change_form(self, request, context, *args, **kwargs):
        """ modelclone not showing Save button because of a bug. This workarounds it. """
        kwargs['add'] = True
        return super().render_change_form(request, context, *args, **kwargs)

    def remaining_spots(self, obj):
        return obj.remaining_spots

    remaining_spots.short_description = "Places disponibles"

    def attendee_list_field(self, obj):
        if obj.id is None:
            return '-'
        return format_html('<a href="%s" target="_new">Llista d\'assistencia</a>' % reverse('admin:attendee-list',
                                                                                            kwargs={'_id': obj.id}))
    attendee_list_field.allow_tags = True
    attendee_list_field.short_description = 'Exportar'

    def attendee_list(self, request, _id):
        import weasyprint
        import django.template.loader as loader
        from django.conf import settings
        import os
        temp = loader.get_template('admin/attendee_list.html')
        content = temp.render(
            {
                'assistants': Activity.objects.get(pk=_id).enrolled.all(),
                'activity': Activity.objects.get(pk=_id)
            }
        )
        # dynamic_css = loader.get_template('admin/attendee-list-pdf.css')

        pdf = weasyprint.HTML(string=content.encode('utf-8'))

        """
        About this way of generating the CSS:
        Turns out that if you place the @page inside the HTML, or
        through weasyprint.CSS(string="css contents"), it doesn't
        apply the attribute at all.
        Only using filename or url attributes worked, so far.
        That's why even for a single variable we created a URL
        to dynamically generate the CSS."""
        css = weasyprint.CSS(url=request.build_absolute_uri(reverse('attendee_list_pdf_css')))
        response = HttpResponse(pdf.write_pdf(stylesheets=[css]), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="llista_assistencia.pdf"'
        return response

    def attendee_filter_field(self, obj):
        if obj.id is None:
            return '-'
        base_url = reverse('admin:coopolis_user_changelist')
        return mark_safe(u'<a href="%s?enrolled_activities__exact=%d">Inscrites</a>' % (
            base_url, obj.id))

    attendee_filter_field.short_description = 'Llistat'

    def send_reminder_field(self, obj):
        if obj.id is None:
            return '-'
        url = reverse('admin:send-activity-reminder', kwargs={'_id': obj.id})
        return mark_safe(
            "<a href=\"{0}\">Enviar e-mails</a>".format(url))

    send_reminder_field.short_description = "Recordatori"

    def send_reminder(self, request, _id):
        # Confirmation page in admin inspired by: https://gist.github.com/rsarai/d475c766871f40e52b8b4d1b12dedea2
        from django.template.response import TemplateResponse
        obj = Activity.objects.get(id=_id)
        if request.method == 'POST':
            mail_to_bcc = set()
            for participant in obj.enrolled.all():
                mail_to_bcc.add(participant.email)
            self._send_confirmation_email(mail_to_bcc, obj, request)
            self.message_user(request, "Recordatoris enviats correctament.")
            return HttpResponseRedirect("../../")

        context = {
            **self.admin_site.each_context(request),
            'obj': obj,
            'opts': self.model._meta,
        }
        return TemplateResponse(
            request, 'admin/reminder_confirmation.html', context)

    @staticmethod
    def _send_confirmation_email(mail_to_bcc, activity, request):
        # TODO: Funció molt similar a la que hi ha a EnrollActivityView, unificar-les.
        from django.core.mail.message import EmailMultiAlternatives
        from django.utils.html import strip_tags

        context = Context({
            'activity': activity,
            'absolute_url': request.build_absolute_uri(reverse('my_activities')),
            'contact_email': config.CONTACT_EMAIL,
            'contact_number': config.CONTACT_PHONE_NUMBER,
            'request': request,
        })
        template = Template(config.EMAIL_ENROLLMENT_CONFIRMATION)
        html_content = template.render(context)
        text_content = strip_tags(html_content)

        mail_to = {config.EMAIL_FROM_ENROLLMENTS}
        if settings.DEBUG:
            mail_to.add(config.EMAIL_TO_DEBUG)

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(
            config.EMAIL_ENROLLMENT_CONFIRMATION_SUBJECT.format(activity.name),
            text_content,
            config.EMAIL_FROM_ENROLLMENTS,
            mail_to,
            mail_to_bcc
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
