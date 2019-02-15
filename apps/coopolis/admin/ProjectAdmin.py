#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User
from simple_history.admin import SimpleHistoryAdmin


class ProjectAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'web', 'mail', 'phone', 'project_responsible', 'registration_date', 'subsidy_period')
    search_fields = ('name', 'web', 'mail', 'phone', 'project_responsible', 'registration_date', 'subsidy_period',
                     'object_finality', 'project_origins', 'solves_necessities', 'social_base', 'sector')
    list_filter = (('project_responsible', admin.RelatedOnlyFieldListFilter), 'registration_date', 'subsidy_period',
                   'sector')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def _users(self, obj):
        return obj.projects.all().count()
