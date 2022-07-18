from django.contrib import admin
from django.conf import settings

from apps.coopolis.models import (
    User, ActivityPoll,
)
from .UserAdmin import UserAdmin
from .ActivityPollAdmin import ActivityPollAdmin


admin.site.register(User, UserAdmin)
admin.site.register(ActivityPoll, ActivityPollAdmin)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
