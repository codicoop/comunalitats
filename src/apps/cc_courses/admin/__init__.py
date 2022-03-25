from django.contrib import admin
from django.conf import settings

from apps.cc_courses.models import (
    Course, Activity, CoursePlace, Entity, Organizer, Cofunding, StrategicLine
)
from .ActivityAdmin import ActivityAdmin, CofundingAdmin, StrategicLineAdmin
from .CourseAdmin import CourseAdmin
from .CoursePlaceAdmin import CoursePlaceAdmin


admin.site.register(Course, CourseAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(CoursePlace, CoursePlaceAdmin)
admin.site.register(Entity)
admin.site.register(Organizer)
admin.site.register(Cofunding, CofundingAdmin)
admin.site.register(StrategicLine, StrategicLineAdmin)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
