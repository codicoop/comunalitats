#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User, Project
from cc_courses.models import Course, Activity
from django.contrib.auth.models import Group
from .ActivityAdmin import ActivityAdmin
from .CourseAdmin import CourseAdmin
from .ProjectAdmin import ProjectAdmin
from .UserAdmin import UserAdmin

admin.site.site_header = "Coópolis Backoffice"
admin.site.site_title = "Coópolis backoffice"
admin.site.index_title = "Benvingut!"

admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Activity, ActivityAdmin)
