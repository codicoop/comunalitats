#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dev import *

# Local strings
PROJECT_NAME = "Coop Maresme"
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
ALLOWED_HOSTS = ['serveis.coopmaresme.cat', 'localhost',]
USE_X_FORWARDED_HOST = True

# Wasabi cloud storage configuration
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = 'ateneus-coopmaresme'
AWS_S3_CUSTOM_DOMAIN = f's3.eu-central-1.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}'
AWS_S3_ENDPOINT_URL = 'https://s3.eu-central-1.wasabisys.com'
EXTERNAL_MEDIA_PATH = 'media'
EXTERNAL_STATIC = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/local'  # In templates use {% external_static "/logo.png" %}

# E-mail server configuration
EMAIL_HOST = 'smtp-es.securemail.pro'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info@coopmaresme.cat'
EMAIL_HOST_PASSWORD = 'Mataro2018'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'info@coopmaresme.cat'
EMAIL_SUBJECT_PREFIX = f'[{PROJECT_NAME}]'
# If it fails, it can be sent by traditional SMTP without SSL nor TLS, with:
# EMAIL_HOST = 'authsmtp.coopmaresme.cat'
# EMAIL_PORT = 25 # or 587

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ateneus_coopmaresme',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    }
}
