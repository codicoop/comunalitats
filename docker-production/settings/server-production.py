#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dev import *

# Local strings
PROJECT_NAME = "Coòpolis"
ADMIN_HEADER = "Back-office de "+PROJECT_NAME
GRAPPELLI_ADMIN_TITLE = "Back-office de "+PROJECT_NAME

# Instance configuration
SECRET_KEY = 'ksdjfklsajdflas flkdjsa flñkjdsa fñlsj'
DEBUG = False
# https://github.com/fabiocaccamo/django-maintenance-mode
# Can also be enabled with: python manage.py maintenance_mode <on|off>
# MAINTENANCE_MODE = True
# MAINTENANCE_MODE_IGNORE_ADMIN_SITE = False
# MAINTENANCE_MODE_IGNORE_SUPERUSER = False
# MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = ('127.0.0.1',)
ALLOWED_HOSTS = ['serveis.bcn.coop', 'localhost',]
USE_X_FORWARDED_HOST = True

# Wasabi cloud storage configuration
AWS_ACCESS_KEY_ID = 'ZRUPD0YYGASZM4LEQI9S'
AWS_SECRET_ACCESS_KEY = 'cAle1LeDl8LoV2PLO46MvnckObqzszm69Tw3fwAn'
AWS_STORAGE_BUCKET_NAME = 'ateneus-coopolis'
AWS_S3_CUSTOM_DOMAIN = f's3.eu-central-1.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}'
AWS_S3_ENDPOINT_URL = 'https://s3.eu-central-1.wasabisys.com'
EXTERNAL_MEDIA_PATH = 'media'
EXTERNAL_STATIC = AWS_S3_ENDPOINT_URL+"/"+AWS_STORAGE_BUCKET_NAME+"/local"  # In templates use {% external_static "/logo.png" %}

# E-mail server configuration
EMAIL_HOST = 'smtp01.correowebseguro.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'web@bcn.coop'
EMAIL_HOST_PASSWORD = 'c00p0l1s_2017'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'web@bcn.coop'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'coopolis',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    }
}
