#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'last_name', 'first_name', 'email', 'project')
    search_fields = ('id_number', 'last_name', 'first_name', 'email', 'residence_town',
                     'residence_district', 'phone_number', 'cooperativism_knowledge', 'adreca_nom_via')
    list_filter = ('gender', 'project', 'residence_town', 'residence_district', 'is_staff')
    exclude = ('user_permissions', 'groups', 'is_confirmed', 'password')
    readonly_fields = ('last_login',)
