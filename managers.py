#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import UserManager


class CCUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)
