#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django import template


def can_enroll(enrollable, individual):
    return individual not in enrollable.enrolled.all() and enrollable.remaining_spots > 0


register = template.Library()
register.filter('can_enroll', can_enroll)
