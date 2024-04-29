from django.contrib import admin

from apps.projects.models import (
    Project, ProjectStage, EmploymentInsertion, StageSubtype,
)
from .ProjectAdmin import (
    ProjectAdmin, ProjectStageAdmin, EmploymentInsertionAdmin,
    StageSubtypeAdmin,
)


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(EmploymentInsertion, EmploymentInsertionAdmin)
admin.site.register(StageSubtype, StageSubtypeAdmin)
