from django.contrib import admin

from apps.cc_users.models import User
from .UserAdmin import UserAdmin


admin.site.register(User, UserAdmin)