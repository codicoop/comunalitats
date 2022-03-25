from django.contrib import admin
from django.conf import settings

from apps.coopolis.models import (
    User, Project, ProjectStage, Derivation, EmploymentInsertion,
    ActivityPoll, StageSubtype,
)
from .ProjectAdmin import (
    ProjectAdmin, ProjectStageAdmin, DerivationAdmin, EmploymentInsertionAdmin,
    StageSubtypeAdmin, ProjectFile, ProjectFileAdmin,
)
from .ProjectsFollowUpAdmin import ProjectsConstitutedAdmin
from .UserAdmin import UserAdmin
from .ActivityPollAdmin import ActivityPollAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(Derivation, DerivationAdmin)
admin.site.register(EmploymentInsertion, EmploymentInsertionAdmin)
admin.site.register(ActivityPoll, ActivityPollAdmin)
admin.site.register(StageSubtype, StageSubtypeAdmin)
admin.site.register(ProjectFile, ProjectFileAdmin)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
