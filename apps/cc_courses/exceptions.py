#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EnrollToActivityNotValidException(Exception):
    """Raise when some not-permitted enrollment is done (possibly already enrolled)"""
