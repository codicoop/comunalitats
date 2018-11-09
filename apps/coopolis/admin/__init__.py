#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User, Project
from cc_courses.models import Course, Activity, CourseCategory, CoursePlace
from .ActivityAdmin import ActivityAdmin
from .CourseAdmin import CourseAdmin
from .ProjectAdmin import ProjectAdmin
from .UserAdmin import UserAdmin
from .CourseCategoryAdmin import CourseCategoryAdmin
from .CoursePlaceAdmin import CoursePlaceAdmin


class CoopolisAdmin(admin.AdminSite):
    site_header = "Coópolis Backoffice"
    site_title = "Coópolis backoffice"
    index_title = "Hola!"


coopolis_admin_site = CoopolisAdmin(name='coopolis_admin')

coopolis_admin_site.register(User, UserAdmin)
coopolis_admin_site.register(Project, ProjectAdmin)
coopolis_admin_site.register(Course, CourseAdmin)
coopolis_admin_site.register(Activity, ActivityAdmin)
coopolis_admin_site.register(CourseCategory, CourseCategoryAdmin)
coopolis_admin_site.register(CoursePlace, CoursePlaceAdmin)
