from django.contrib import admin
from django.conf import settings

from apps.coopolis.models import (
    User, Project, ProjectStage, Derivation, EmploymentInsertion,
    ProjectsFollowUp, ProjectsConstituted, ActivityPoll, StageSubtype,
)
from apps.cc_courses.models import (
    Course, Activity, CoursePlace, Entity, Organizer, Cofunding, StrategicLine
)
from .ActivityAdmin import ActivityAdmin, CofundingAdmin, StrategicLineAdmin
from .CourseAdmin import CourseAdmin
from .ProjectAdmin import (
    ProjectAdmin, ProjectStageAdmin, DerivationAdmin, EmploymentInsertionAdmin,
    StageSubtypeAdmin, ProjectFile, ProjectFileAdmin,
)
from .ProjectsFollowUpAdmin import (
    ProjectsFollowUpAdmin, ProjectsConstitutedAdmin
)
from .UserAdmin import UserAdmin
from .CoursePlaceAdmin import CoursePlaceAdmin
from .ActivityPollAdmin import ActivityPollAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(CoursePlace, CoursePlaceAdmin)
admin.site.register(Entity)
admin.site.register(Organizer)
admin.site.register(Derivation, DerivationAdmin)
admin.site.register(EmploymentInsertion, EmploymentInsertionAdmin)
admin.site.register(ProjectsConstituted, ProjectsConstitutedAdmin)
admin.site.register(Cofunding, CofundingAdmin)
admin.site.register(StrategicLine, StrategicLineAdmin)
admin.site.register(ActivityPoll, ActivityPollAdmin)
admin.site.register(StageSubtype, StageSubtypeAdmin)
admin.site.register(ProjectFile, ProjectFileAdmin)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
