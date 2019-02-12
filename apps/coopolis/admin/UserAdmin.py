#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'last_name', 'first_name', 'email', 'project')
