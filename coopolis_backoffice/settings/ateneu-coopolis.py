from .dev import *

# Local strings
PROJECT_NAME = "Coopolis"
ADMIN_HEADER = "Back-office de "+PROJECT_NAME
GRAPPELLI_ADMIN_TITLE = "Back-office de "+PROJECT_NAME
ALLOWED_HOSTS = ['ateneus-develop.codi.coop', '127.0.0.1', ]
ABSOLUTE_URL = f"http://{ALLOWED_HOSTS[0]}:5001"

# Instance configuration
DEBUG = True
# SECRET_KEY = 'something'
# https://github.com/fabiocaccamo/django-maintenance-mode
# Can also be enabled with: python manage.py maintenance_mode <on|off>
# MAINTENANCE_MODE = True
# MAINTENANCE_MODE_IGNORE_ADMIN_SITE = False
# MAINTENANCE_MODE_IGNORE_SUPERUSER = False
# MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = ('127.0.0.1',)
# ALLOWED_HOSTS = ['example.com',]
# USE_X_FORWARDED_HOST = True

# Wasabi cloud storage configuration
AWS_ACCESS_KEY_ID = '8TG4JC6IAIXMCJ0XRUAD'
AWS_SECRET_ACCESS_KEY = 'LGHPy3K11ks2VmZhIdDrO9HKY8Ehqy8DW4WNlE7O'
AWS_STORAGE_BUCKET_NAME = 'ateneus-demo'
AWS_S3_CUSTOM_DOMAIN = f's3.eu-central-1.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}'
AWS_S3_ENDPOINT_URL = 'https://s3.eu-central-1.wasabisys.com'
EXTERNAL_MEDIA_PATH = 'media'
EXTERNAL_STATIC = AWS_S3_ENDPOINT_URL+"/"+AWS_STORAGE_BUCKET_NAME+"/local"  # In templates use {% external_static "/logo.png" %}

# E-mail server configuration
# EMAIL_HOST = 'smtp01.correowebseguro.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'web@bcn.coop'
# EMAIL_HOST_PASSWORD = 'c00p0l1s_2017'
# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'web@bcn.coop'
# EMAIL_SUBJECT_PREFIX = f'[{PROJECT_NAME}]'

# E-mail server configuration
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'ateneus.te2@gmail.com'
# EMAIL_HOST_PASSWORD = 'At3n3uT&2'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'ateneus.te2@gmail.com'
# EMAIL_SUBJECT_PREFIX = f'[{PROJECT_NAME}]'
# MAILING_MANAGER_DEFAULT_FROM = DEFAULT_FROM_EMAIL

# E-mail server configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'serveis.ateneucoopte@gmail.com'
EMAIL_HOST_PASSWORD = '#Amposta2020'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'serveis.ateneucoopte@gmail.com'
EMAIL_SUBJECT_PREFIX = f'[{PROJECT_NAME}]'
MAILING_MANAGER_DEFAULT_FROM = DEFAULT_FROM_EMAIL


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'coopcamp',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    }
}
