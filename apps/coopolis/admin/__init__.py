#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings

from coopolis.models import User, Project, ProjectStage, Derivation, EmploymentInsertion, StagesByAxis, \
    ProjectsFollowUp, ProjectsConstituted
from cc_courses.models import Course, Activity, CoursePlace, Entity, Organizer
from .ActivityAdmin import ActivityAdmin
from .CourseAdmin import CourseAdmin
from .ProjectAdmin import ProjectAdmin, ProjectStageAdmin, DerivationAdmin, EmploymentInsertionAdmin, \
    ProjectStageAdminAxis
from .ProjectsFollowUpAdmin import ProjectsFollowUpAdmin, ProjectsConstitutedAdmin
from .UserAdmin import UserAdmin
from .CoursePlaceAdmin import CoursePlaceAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(StagesByAxis, ProjectStageAdminAxis)
admin.site.register(Course, CourseAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(CoursePlace, CoursePlaceAdmin)
admin.site.register(Entity)
admin.site.register(Organizer)
admin.site.register(Derivation, DerivationAdmin)
admin.site.register(EmploymentInsertion, EmploymentInsertionAdmin)
admin.site.register(ProjectsFollowUp, ProjectsFollowUpAdmin)
admin.site.register(ProjectsConstituted, ProjectsConstitutedAdmin)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
