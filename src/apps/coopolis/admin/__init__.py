from django.contrib import admin

from apps.polls.models import ActivityPoll
from apps.cc_users.models import User
from .UserAdmin import UserAdmin
from .ActivityPollAdmin import ActivityPollAdmin


admin.site.register(User, UserAdmin)
admin.site.register(ActivityPoll, ActivityPollAdmin)