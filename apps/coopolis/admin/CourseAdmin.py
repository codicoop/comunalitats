#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django_summernote.admin import SummernoteModelAdmin


class CourseAdmin(SummernoteModelAdmin):
    list_display = ('title',)
    summernote_fields = ('objectives',)


