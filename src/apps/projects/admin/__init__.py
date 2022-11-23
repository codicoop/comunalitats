from django.contrib import admin

from apps.projects.models import (
    Project, ProjectStage, Derivation, EmploymentInsertion, StageSubtype,
)
from .ProjectAdmin import (
    ProjectAdmin, ProjectStageAdmin, DerivationAdmin, EmploymentInsertionAdmin,
    StageSubtypeAdmin, ProjectFileAdmin,
)
from .ProjectsFollowUpAdmin import ProjectsFollowUpService, ProjectsConstitutedService


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(Derivation, DerivationAdmin)
admin.site.register(EmploymentInsertion, EmploymentInsertionAdmin)
admin.site.register(StageSubtype, StageSubtypeAdmin)
