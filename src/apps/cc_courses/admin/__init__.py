from django.contrib import admin
from django.conf import settings

from apps.cc_courses.models import (
    Course, Activity, CoursePlace, Entity, Organizer
)
from .ActivityAdmin import ActivityAdmin
from .CourseAdmin import CourseAdmin
from .CoursePlaceAdmin import CoursePlaceAdmin


admin.site.register(Course, CourseAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(CoursePlace, CoursePlaceAdmin)
admin.site.register(Entity)
admin.site.register(Organizer)
