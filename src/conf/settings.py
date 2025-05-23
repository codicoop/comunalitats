import environ
import os

from django.core.management.utils import get_random_secret_key

env = environ.Env()
# False if not in os.environ
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
# Instance's absolute URL (given we're not using Sites framework)
ABSOLUTE_URL = env.str('ABSOLUTE_URL', default="")
# Necessari per tal que al recuperar password faci servir el mateix host que
# la URL que s'està visitant. Si això fos False, caldria activar el Sites
# Framework i configurar el nom del host.
USE_X_FORWARDED_HOST = True

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env.str('SECRET_KEY', default=get_random_secret_key())

# Variables for non-interactive superuser creation
DJANGO_SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL", default=None)
DJANGO_SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD", default=None)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME', default="postgres"),
        'USER': env.str('DB_USER', default="postgres"),
        'PASSWORD': env.str('DB_PASSWORD', default=""),
        'HOST': env.str('DB_HOST', default=""),
        'PORT': env.int('DB_PORT', default=5432),
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sendgrid
SENDGRID_API_KEY = env("SENDGRID_API_KEY", default="")
SENDGRID_SANDBOX_MODE_IN_DEBUG = env(
    "SENDGRID_SANDBOX_MODE_IN_DEBUG", bool, default=False
)
SENDGRID_TRACK_EMAIL_OPENS = env("SENDGRID_TRACK_EMAIL_OPENS", bool, default=False)
SENDGRID_TRACK_CLICKS_HTML = env("SENDGRID_TRACK_CLICKS_HTML", bool, default=False)
SENDGRID_TRACK_CLICKS_PLAIN = env("SENDGRID_TRACK_CLICKS_PLAIN", bool, default=False)

# SMTP
EMAIL_HOST = env.str('EMAIL_HOST', default="")
EMAIL_PORT = env.int('EMAIL_PORT', default="")
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default="")
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default="")
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=False)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
MAILING_MANAGER_DEFAULT_FROM = env.str(
    'MAILING_MANAGER_DEFAULT_FROM',
    default=None,
)
# Mails will be queued instead of sent immediately:
MAILQUEUE_QUEUE_UP = env.bool("MAILQUEUE_QUEUE_UP", default=False)
# MAIL-QUEUE SETTINGS
MAILQUEUE_CELERY = False
# Maximum amount of emails to send during each queue run
MAILQUEUE_LIMIT = 10
# If MAILQUEUE_STORAGE is set to True, will ignore your default storage
# settings and use Django's filesystem storage instead (stores them in
# MAILQUEUE_ATTACHMENT_DIR)
MAILQUEUE_STORAGE = False
MAILQUEUE_ATTACHMENT_DIR = 'mailqueue-attachments'

# Wasabi cloud storage configuration
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', default="")
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', default="")
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', default="")
AWS_S3_ENDPOINT_URL = env.str('AWS_S3_ENDPOINT_URL', default="")
AWS_DEFAULT_ACL = env.str('AWS_DEFAULT_ACL', default="")
AWS_PUBLIC_MEDIA_LOCATION = env.str('AWS_PUBLIC_MEDIA_LOCATION', default="")
AWS_S3_BASE_DOMAIN = env.str('AWS_S3_BASE_DOMAIN', default='')
AWS_S3_CUSTOM_DOMAIN = f"{AWS_S3_BASE_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}"
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
EXTERNAL_STATIC = AWS_S3_ENDPOINT_URL+"/"+AWS_STORAGE_BUCKET_NAME+"/local"
# In templates use {% external_static "/logo.png" %}
AWS_PRIVATE_MEDIA_LOCATION = env.str('AWS_PRIVATE_MEDIA_LOCATION', default="")
MEDIA_FILE_OVERWRITE = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Local strings
PROJECT_NAME = env.str("PROJECT_NAME", "")
ADMIN_HEADER = env.str("ADMIN_HEADER", "")
GRAPPELLI_ADMIN_TITLE = env.str("GRAPPELLI_ADMIN_TITLE", "")

# Application definition
INSTALLED_APPS = [
    'django_extensions',
    'maintenance_mode',
    'django.contrib.postgres',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.base',
    'apps.dataexports',
    'apps.cc_users',
    'apps.cc_courses',
    'apps.facilities_reservations',
    'apps.coopolis',
    'apps.projects',
    'apps.polls',
    'apps.towns',
    'grappelli.dashboard',
    'grappelli',
    'tagulous',
    'logentry_admin',
    'constance.backends.database',
    'constance',
    'django_object_actions',
    'django.contrib.admin',
    'django_summernote',
    'storages',
    'easy_thumbnails',
    'modelclone',
    'apps.coopolis.templatetags.my_tag_library',
    'mailqueue',
    'mailing_manager',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.coopolis.context_processors.settings_values',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.cc_users.authentication_backend.IdNumberBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ca'

TIME_ZONE = 'Europe/Andorra'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# For Tagulous
SERIALIZATION_MODULES = {
    'xml':    'tagulous.serializers.xml_serializer',
    'json':   'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml':   'tagulous.serializers.pyyaml',
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "assets"),
# ]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = 'loginsignup'
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'cc_users.User'
DEV_SETTINGS_MODULE = 'conf.settings'

FIXTURES_PATH_TO_COURSE_IMAGES = 'test-images/coopolis-courses'

# Constance
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_SUPERUSER_ONLY = False
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    # Courses
    'CONTENT_COURSES_INTRODUCTION': (
        "Disposem d’una oferta regular de formació en economia"
        " social i cooperativisme per a tots els públics, tant per a aquelles "
        "persones que tenen ganes d’apropar-se a l’economia social i "
        "solidària, com per a aquelles persones o col·lectius que estan "
        "pensant en constituir el seu propi projecte econòmic. "
        "També oferim formacions"
        " descentralitzades en altres espais comunitaris i seus de l’economia "
        "social i solidària barcelonina.",
        "Formació: text d'introducció."),
    'CONTENT_COURSES_DETAIL': (
        "Veure les activitats",
        "Text de botó que porta a la informació d'un curs."),
    # Home
    'CONTENT_HOME_COURSES_TITLE': (
        "Formació i activitats",
        "Portada, títol del bloc que informa sobre la formació."),
    'CONTENT_HOME_COURSES_TEXT': (
        "Disposem d’una oferta regular de formació en economia solidària i "
        "cooperativisme per a tots els públics, tant per a aquelles persones "
        "que tenen ganes d’apropar-se a l’ESS per primera vegada, els "
        "col·lectius que estan engegant un projecte, i cooperatives que volen "
        "consolidar la seva activitat incorporant nous coneixements "
        "especialitzats.",
        "Portada, títol del bloc que informa sobre la formació."),
    'CONTENT_HOME_INTRODUCTION': (
        "<p><strong>Benvingudes a la web de gestió d’inscripcions "
        "de la comunalitat!</strong></p><p>Cal que us doneu d’alta "
        "amb les vostres dades personals, i podreu realitzar les inscripcions "
        "de les formacions.</p>",
        "Text d'introducció de la home."),
    'CONTENT_COURSES': (
        "Oferta formativa",
        "Text de botó que porta a la llista de cursos."),
    # Sign up
    'CONTENT_SIGNUP_LEGAL1': (
        "Paràgraf text legal #1",
        'Casella per acceptar #1.'),
    'CONTENT_SIGNUP_LEGAL2': (
        "Sóc coneixedor/a del caràcter de subvenció pública amb la qual es "
        "finança l’actuació en la qual vull participar, mitjançant el "
        "cofinançament del Ministeri d’Ocupació i Seguretat Social, i "
        "l’Ajuntament de Barcelona.",
        'Casella per acceptar #2.'),
    # Configuration
    'DISABLE_FOOTER_AND_HEADER': (
        False,
        "Ocultar l'encapçalament i peu de pàgina a l'aplicació. Activa "
        "aquesta opció si vols 'incrustar' l'aplicació dins d'una altra "
        "pàgina o aplicació web.",
        bool,
    ),
    'EMAIL_TO_DEBUG': (
        'pere@codi.coop', 'Correu per fer proves d\'enviaments.'),
    'PROJECT_NAME': ("Comunalitat", "Nom curt de la comunalitat."),
    'PROJECT_FULL_NAME': (
        "Comunalitat per la xarxa econòmica urbana",
        "Nom llarg, p.ex.: 'Comunalitat de Vic'. També "
        "hi podeu posar el mateix que al nom curt, si voleu."),
    'PROJECT_CONTACT_URL': (
        "https://example.com",
        "Enllaç a la pàgina de contacte de la comunalitat. Apareix a peu de "
        "pàgina."),
    'PROJECT_LEGAL_URL': (
        "https://example.com",
        "Enllaç a la pàgina de les condicions legals de la comunalitat. Apareix a: "
        "missatge d'acceptar cookies, peu de pàgina, i al text d'acceptació "
        "de condicions legals del formulari d'alta."),
    'PROJECT_WEBSITE_URL': (
        "https://example.com",
        "Enllaç a la pàgina principal de la comunalitat. Apareix al menú "
        "principal."),
    'CONTACT_PHONE_NUMBER': (
        "93 XXX XX XX",
        "Apareix al correu que s'envia a la gent que s'inscriu a activitats, "
        "perquè sàpiguen on contactar si tenen dubtes. De la mateixa manera "
        "apareix al correu que s'envia quan envieu un recordatori a tota la "
        "gent inscrita a una activitat."),
    'PROJECT_FACEBOOK_URL': (
        "",
        "Si s'indica la URL del perfil de Facebook, apareixerà a la plantilla "
        "dels correus electrònics."),
    'PROJECT_TWITTER_URL': (
        "",
        "Si s'indica la URL del perfil de Twitter, apareixerà a la plantilla "
        "dels correus electrònics."),
    'PROJECT_INSTAGRAM_URL': (
        "",
        "Si s'indica la URL del perfil d'Instagram, apareixerà a la plantilla "
        "dels correus electrònics."),
    'CONTACT_EMAIL': (
        "hola@example.com",
        "Apareix al correu que s'envia a la persona que s'ha inscrit a una "
        "activitat (i al de recordatori que s'envia massivament des de l'admin) "
        "per indicar que si tenen dubtes, escriguin a aquest correu."),
    'ATTENDEE_LIST_FOOTER_IMG': (
        "https://example.com/footer.png",
        "URL de la imatge pel peu de pàgina del llistat d'assistència."),
    'CUSTOM_STYLESHEET_URL': (
        "",
        "URL a un full d'estils que d'inclourà en última posició, de manera "
        "que sobreescrigui la resta d'estils.",
    ),
}
CONSTANCE_CONFIG_FIELDSETS = {
    'Configuració': (
        'PROJECT_NAME', 'PROJECT_FULL_NAME',
        'PROJECT_WEBSITE_URL', 'PROJECT_LEGAL_URL', 'PROJECT_CONTACT_URL',
        'CONTACT_PHONE_NUMBER', 'CONTACT_EMAIL',
        'PROJECT_FACEBOOK_URL', 'PROJECT_TWITTER_URL', 'PROJECT_INSTAGRAM_URL'
    ),
    "Apartat Portada": (
        'CONTENT_HOME_COURSES_TITLE', 'CONTENT_HOME_COURSES_TEXT',
        'CONTENT_HOME_INTRODUCTION', 'CONTENT_COURSES'
    ),
    "Apartat Formació": ('CONTENT_COURSES_INTRODUCTION', 'CONTENT_COURSES_DETAIL'),
    "Formulari d'alta": ('CONTENT_SIGNUP_LEGAL1', 'CONTENT_SIGNUP_LEGAL2',),
    "Variables avançades": (
        'CUSTOM_STYLESHEET_URL',
        'DISABLE_FOOTER_AND_HEADER',
        'ATTENDEE_LIST_FOOTER_IMG',
        'EMAIL_TO_DEBUG',
    ),
}

# CC Courses

COURSES_LIST_VIEW_CLASS = 'apps.coopolis.views.CoopolisCoursesListView'

FIXTURE_FACTORIES = [
    ('apps.coopolis.tests.fixtures.UserFactory', {}),
    ('apps.coopolis.tests.fixtures.ProjectFactory', {}),
    ('apps.cc_courses.tests.fixtures.CourseFactory', {}),
    ('apps.cc_courses.tests.fixtures.EntityFactory', {}),
    ('apps.cc_courses.tests.fixtures.CoursePlaceFactory', {}),
    ('apps.cc_courses.tests.fixtures.ActivityFactory', {
        'number': 500
    }),
]

PROJECT_STATUS = (
    ('PENDENT', "Pendent d’enviar proposta de trobada"),
    ('ENVIAT', "Enviat email amb proposta de data per trobar-nos"),
    ('CONCERTADA', "Data de trobada concertada"),
    ('ACOLLIT', "Acollida realitzada"),
    ('PAUSA', "Acompanyament en pausa"),
    ('CANCEL', "Acompanyament cancel·lat")
)
CALENDAR_COLOR_FOR_ACTIVITIES_OUTSIDE = '#808080'

# Grappeli
# (https://django-grappelli.readthedocs.io/en/latest/customization.html)
GRAPPELLI_SWITCH_USER = False
GRAPPELLI_INDEX_DASHBOARD = 'apps.coopolis.dashboard.MyDashboard'

THUMBNAIL_ALIASES = {
    '': {
        'course_list': {'size': (150, 200), 'scale-crop': True},
    },
}
THUMBNAIL_DEFAULT_STORAGE = 'apps.cc_lib.storages.MediaStorage'

# Maintenance mode
MAINTENANCE_MODE = env.bool("MAINTENANCE_MODE", default=False)
MAINTENANCE_MODE_STATE_BACKEND = "maintenance_mode.backends.DefaultStorageBackend"
