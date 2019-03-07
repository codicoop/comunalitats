#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User, ProjectStage
from django.utils.safestring import mark_safe
from coopolis.mixins import ExportCsvMixin


class ProjectAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'web', 'mail', 'phone', 'registration_date', 'stages_field')
    search_fields = ('name', 'web', 'mail', 'phone', 'registration_date', 'object_finality', 'project_origins',
                     'solves_necessities', 'social_base', 'sector')
    list_filter = ('registration_date', 'sector')
    actions = ["export_as_csv"]

    def stages_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s?project__exact=%d">Veure</a>' % (
            'coopolis', 'projectstage', obj.id))

    stages_field.short_description = 'Fases'


class ProjectStagePartnersInline(admin.TabularInline):
    model = ProjectStage.involved_partners.through
    verbose_name = "persona que ha participat en aquesta fase"
    extra = 0


class ProjectStageAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('date_start', 'stage_responsible', 'project_field', 'stage', 'axis', 'organizer', 'subsidy_period')
    list_filter = ('subsidy_period', ('stage_responsible', admin.RelatedOnlyFieldListFilter), 'project', 'date_start',
                   'axis', 'organizer')
    actions = ["export_as_csv"]
    exclude = ('involved_partners', )
    inlines = [ProjectStagePartnersInline, ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "stage_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def project_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s/%d/change">%s</a>' % (
            'coopolis', 'project', obj.project.id, obj.project))

    project_field.short_description = 'Projecte'
