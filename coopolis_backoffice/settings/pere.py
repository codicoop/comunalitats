#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dev import *

DEBUG = True
AWS_ACCESS_KEY_ID = 'WNN4APXU4EJIKTBJSU6T'
AWS_SECRET_ACCESS_KEY = 'eFMXkfhaODCzrC1jzFduM6nNABzlELvGHN30eiZX'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_USE_TLS = True
del EMAIL_BACKEND
DEFAULT_FROM_EMAIL = 'hola@codi.coop'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'coopolis',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    },
    'old': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coopolis_old',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}