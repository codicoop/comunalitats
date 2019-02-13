#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User, Project
from cc_courses.models import Course, Activity, CoursePlace, Entity
from .ActivityAdmin import ActivityAdmin
from .CourseAdmin import CourseAdmin
from .ProjectAdmin import ProjectAdmin
from .UserAdmin import UserAdmin
from .CoursePlaceAdmin import CoursePlaceAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(CoursePlace, CoursePlaceAdmin)
admin.site.register(Entity)
