#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.html import format_html


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'my_url_field',)

    def my_url_field(self, obj):
        return format_html('<a href="%s%s">%s</a>' % ('http://url-to-prepend.com/', obj.title, obj.title))
    my_url_field.allow_tags = True
    my_url_field.short_description = 'Column description'
