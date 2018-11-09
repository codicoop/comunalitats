#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from django.urls import path, reverse
from cc_courses.models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'my_url_field',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                r'<id>/attendee-list/',
                self.admin_site.admin_view(self.attendee_list),
                name='attendee-list',
            ),
        ]
        return custom_urls + urls

    def my_url_field(self, obj):
        return format_html('<a href="%s" target="_new">Llista d\'assistencia</a>' % reverse('admin:attendee-list', kwargs={'id': obj.id}))

    my_url_field.allow_tags = True
    my_url_field.short_description = 'Column description'

    def attendee_list(self, request, id):
        import weasyprint
        import django.template.loader as loader
        temp = loader.get_template('admin/attendee_list.html')
        content = temp.render({'assistants': Course.objects.get(pk=id).enrolled.all()})
        pdf = weasyprint.HTML(string=content.encode('utf-8'))
        response = HttpResponse(pdf.write_pdf(), content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="llista_assistencia.pdf"'
        response['Content-Disposition'] = 'filename="llista_assistencia.pdf"'
        return response
