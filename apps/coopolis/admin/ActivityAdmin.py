#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.html import format_html
from django.http import HttpResponse
from django.urls import path, reverse
from cc_courses.models import Activity
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin


class ActivityAdmin(SummernoteModelAdmin):
    list_display = ('date_start', 'spots', 'remaining_spots', 'name', 'attendee_filter_field', 'attendee_list_field',)
    readonly_fields = ('attendee_list_field',)
    summernote_fields = ('objectives',)
    search_fields = ('date_start', 'name', 'objectives',)
    list_filter = ('course', 'date_start', 'justification', 'entity', 'axis', 'place', 'for_minors',)
    fieldsets = (
        (None, {
            'fields': ('course', 'name', 'objectives', 'place', 'date_start', 'date_end', 'starting_time',
                       'ending_time', 'spots', 'enrolled', 'entity', 'organizer')
        }),
        ('Dades relatives a activitats per menors', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('for_minors', 'minors_school_name', 'minors_school_cif', 'minors_grade', 'minors_participants_number',
                       'minors_teacher'),
        })
    )

    def remaining_spots(self, obj):
        return obj.remaining_spots

    remaining_spots.short_description = "Places disponibles"

    def get_queryset(self, request):
        qs = super(ActivityAdmin, self).get_queryset(request)
        self.request = request
        return qs

    def copy_clipboard_field(self, obj):
        abs_url = self.request.build_absolute_uri(obj.absolute_url)
        return mark_safe("""
    {0} <a href="javascript:copyToClipboard('{0}');"> ─ Copiar &#128203;</a>
    <script>
    function copyToClipboard (str) {{
    var dummy = document.createElement("input");
      document.body.appendChild(dummy);
      dummy.setAttribute("id", "dummy_id");
      document.getElementById("dummy_id").value=str;
      dummy.select();
      document.execCommand("copy");
      document.body.removeChild(dummy);
      alert(str + ' copied.');
    }}
    </script>
    """.format(abs_url))

    copy_clipboard_field.short_description = 'Link a la sessió'

    def copy_clipboard_list_field(self, obj):
        abs_url = self.request.build_absolute_uri(obj.absolute_url)
        return mark_safe("""
    <a href="javascript:copyToClipboard('{0}');">Copiar &#128203;</a>
    <script>
    function copyToClipboard (str) {{
    var dummy = document.createElement("input");
      document.body.appendChild(dummy);
      dummy.setAttribute("id", "dummy_id");
      document.getElementById("dummy_id").value=str;
      dummy.select();
      document.execCommand("copy");
      document.body.removeChild(dummy);
      alert(str + ' copied.');
    }}
    </script>
    """.format(abs_url))

    copy_clipboard_list_field.short_description = 'Link a la sessió'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                r'<_id>/attendee-list/',
                self.admin_site.admin_view(self.attendee_list),
                name='attendee-list',
            ),
        ]
        return custom_urls + urls

    def attendee_list_field(self, obj):
        return format_html('<a href="%s" target="_new">Llista d\'assistencia</a>' % reverse('admin:attendee-list',
                                                                                            kwargs={'_id': obj.id}))
    attendee_list_field.allow_tags = True
    attendee_list_field.short_description = 'Exportar'

    def attendee_list(self, request, _id):
        import weasyprint
        import django.template.loader as loader
        from django.templatetags.static import static
        from django.conf import settings
        import os
        temp = loader.get_template('admin/attendee_list.html')
        content = temp.render(
            {
                'assistants': Activity.objects.get(pk=_id).enrolled.all(),
                'activity': Activity.objects.get(pk=_id)
            }
        )

        pdf = weasyprint.HTML(string=content.encode('utf-8'))
        css = weasyprint.CSS(
            filename=os.path.join(settings.BASE_DIR, '../apps/coopolis/static/styles/attendee-list-pdf.css'))
        response = HttpResponse(pdf.write_pdf(stylesheets=[css]), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="llista_assistencia.pdf"'
        return response

    def attendee_filter_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s?enrolled_activities__exact=%d">Inscrites</a>' % (
            'coopolis', 'user', obj.id))

    attendee_filter_field.short_description = 'Llistat'

    # define the raw_id_fields
    raw_id_fields = ('enrolled',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'm2m': ['enrolled'],
    }
