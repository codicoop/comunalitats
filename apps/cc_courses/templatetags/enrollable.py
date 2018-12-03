#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django import template


def can_enroll(enrollable, individual):
    """
    Can enroll if...
    - This class can enroll
    - The individual is not enrolled yet
    - There are remain available applications
    """
    c_name = enrollable.__module__ + "." + enrollable.__class__.__qualname__
    return c_name in settings.COURSES_CLASSES_CAN_ENROLL \
           and individual not in enrollable.enrolled.all() \
           and enrollable.remain_applications > 0


register = template.Library()
register.filter('can_enroll', can_enroll)
