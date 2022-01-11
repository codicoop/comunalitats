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
# TODO: delete this commented code if it proves to be deprecatred.
# sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../apps')))

# Local strings
PROJECT_NAME = env.str("PROJECT_NAME", "")
ADMIN_HEADER = env.str("ADMIN_HEADER", "")
GRAPPELLI_ADMIN_TITLE = env.str("GRAPPELLI_ADMIN_TITLE", "")
CIRCLE_NAMES = [
    env.str("CIRCLE_NAME_ATENEU", ""),
    env.str("CIRCLE_NAME_1", ""),
    env.str("CIRCLE_NAME_2", ""),
    env.str("CIRCLE_NAME_3", ""),
    env.str("CIRCLE_NAME_4", ""),
    env.str("CIRCLE_NAME_5", ""),
]

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
    'apps.dataexports',
    'apps.cc_users',
    'apps.cc_courses',
    'apps.facilities_reservations',
    'apps.coopolis',
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
    "django_q",
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

AUTH_USER_MODEL = 'coopolis.User'
DEV_SETTINGS_MODULE = 'conf.settings'

# APPS

USERS_APP_TITLE = 'Usuàries'
COURSES_APP_TITLE = "Accions"

FIXTURES_PATH_TO_COURSE_IMAGES = 'test-images/coopolis-courses'

# Constance
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_SUPERUSER_ONLY = False
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    # Configurable modules or features
    'ENABLE_ROOM_RESERVATIONS_MODULE': (
        False, "Activar el mòdul de reserva d'espais", bool),
    'ENABLE_COFUNDED_OPTIONS': (
        False, "Activar el bloc d'opcions per activitats cofinançades", bool),
    'ENABLE_STAGE_SUBTYPES': (
        False, "Mostrar el camp \"Subtipus\" a les justificacions "
               "d'acompanyament.", bool),
    # Courses
    'CONTENT_COURSES_INTRODUCTION': (
        "Des de Coòpolis disposem d’una oferta regular de formació en economia"
        " social i cooperativisme per a tots els públics, tant per a aquelles "
        "persones que tenen ganes d’apropar-se a l’economia social i "
        "solidària, com per a aquelles persones o col·lectius que estan "
        "pensant en constituir el seu propi projecte econòmic. A més de les "
        "activitats a l’espai Coòpolis de Can Batlló, també oferim formacions"
        " descentralitzades en altres espais comunitaris i seus de l’economia "
        "social i solidària barcelonina.",
        "Formació: text d'introducció a la franja blava"),
    # Project
    'CONTENT_PROJECT_INTRODUCTION': (
        "<p>Des de Coòpolis acompanyem projectes en la seva posada en marxa i "
        "constitució com a cooperatives, en aquells aspectes centrals per a la"
        " seva activitat i facilitem eines i recursos per a la seva "
        "consolidació i creixement. També dissenyem itineraris per a la "
        "transformació d’associacions i altres formes d’empreses a "
        "cooperatives.</p>",
        "Apartat Projecte: text d'introducció a la franja blava."),
    'CONTENT_PROJECT_TITLE': (
        "Assessorament de projectes",
        "Apartat Projecte: text d'encapçalament"),
    'CONTENT_PROJECT_INFO': (
        "<p>Per sol·licitar acompanyament per al teu projecte, accedeix amb "
        "el teu compte o crea'n un amb els formularis que hi ha a "
        "continuació.</p>",
        "Aartat Projecte: Text que es mostra a l'apartat si hi accedeix sense "
        "haver fet login"),
    'CONTENT_PROJECT_NEW': (
        "<p>Omple el següent formulari per sol·licitar un acompanyament.</p>",
        "Apartat Projecte: Text que es mostra al formulari per sol·licitar "
        "un acompanyament"),
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
        "<p><strong>Benvingudes a la web de gestió d’inscripcions i "
        "acompanyaments de Coòpolis!</strong></p><p>Cal que us doneu d’alta "
        "amb les vostres dades personals, i podreu realitzar les inscripcions "
        "de les formacions, i sol·licitar assessorament per a la creació de "
        "projectes cooperatius.</p><p><em>(*Si teniu dificultats, podeu "
        "escriure un correu a <a href=\"mailto:inscripcions@bcn.coop\">"
        "inscripcions@bcn.coop</a> o trucar a Coòpolis)</em></p>",
        "Text d'introducció de la home."),
    "CONTENT_HOME_PROJECTS_TITLE": (
        "Acompanyament de projectes",
        "Portada: títol del bloc que informa sobre l'acompanyament de "
        "projectes."),
    "CONTENT_HOME_PROJECTS_TEXT": (
        "Des de Coòpolis acompanyem projectes en la seva posada en marxa i "
        "constitució com a cooperatives, en aquells aspectes centrals per a la"
        " seva activitat i facilitem eines i recursos per a la seva "
        "consolidació i creixement. També dissenyem itineraris per a la "
        "transformació d’associacions i altres formes d’empreses a "
        "cooperatives.",
        "Portada: bloc que informa sobre l'acompanyament de projectes."),
    # Sign up
    'CONTENT_SIGNUP_LEGAL1': (
        "La participació en les activitats de Coòpolis, Ateneu Cooperatiu de "
        "Barcelona, està subjecta a un seguit de condicions que entre altres "
        "aspectes recullen el tractament que es farà de les vostres dades "
        "segons la nova Llei del RGPT i el permís per utilitzar la vostra "
        "imatge per a arxiu i difusió de l'activitat, i mai amb cap ús "
        "comercial.",
        'Casella per acceptar #1.'),
    'CONTENT_SIGNUP_LEGAL2': (
        "Sóc coneixedor/a del caràcter de subvenció pública amb la qual es "
        "finança l’actuació en la qual vull participar, mitjançant el "
        "cofinançament del Ministeri d’Ocupació i Seguretat Social, i "
        "l’Ajuntament de Barcelona.",
        'Casella per acceptar #2.'),
    # E-mails
    'EMAIL_NEW_PROJECT': (
        "Nova sol·licitud d'acompanyament<br />"                          
        "<br />"
        "Nom del projecte: {} <br />"
        "Telèfon de contacte: {} <br />"
        "Correu electrònic de contacte del projecte: {} <br />"
        "Correu electrònic de l'usuari que l'ha creat: {} <br />",
        "Cos del correu que s'envia quan algú sol·licita un acompanyament."),
    'EMAIL_NEW_PROJECT_SUBJECT': (
        "Nova sol·licitud d'acompanyament: {}",
        "Assumpte del correu que s'envia quan algú sol·licita un "
        "acompanyament."),
    'EMAIL_ENROLLMENT_CONFIRMATION': (
        "Inscripció a l'activitat: {} <br />"
        "<br />Dades de l'activitat:<br />"
        "Data: {}<br />"
        "Horari: de {} a {}<br />"
        "Lloc: {}<br />"
        "<br />"
        "Les places son limitades. Si finalment no pots assistir-hi, si us "
        "plau anul·la la teva inscripció. Per fer-ho, pots gestionar les "
        "teves inscripcions accedint al back-office de Coòpolis amb el teu "
        "correu i contrasenya <a href=\"{}\">aquí</a> "
        "o bé contactar-nos al correu electrònic {}, o trucar-nos al {}.",
        "Cos del correu que s'envia quan algú s'inscriu a una activitat"),
    'EMAIL_ENROLLMENT_CONFIRMATION_SUBJECT': (
        "Confirmació d'inscripció a l'activitat: {}",
        "Assumpte del correu que s'envia quan algú s'inscriu a una activitat"),
    'EMAIL_ENROLLMENT_WAITING_LIST': (
        "Inscripció en llista d'espera.",
        "Cos del correu que s'envia quan algú s'inscriu a una activitat i "
        "entra en llista d'espera."),
    'EMAIL_ENROLLMENT_WAITING_LIST_SUBJECT': (
        "Ets en llista d'espera per l'activitat: {}",
        "Assumpte del correu que s'envia quan algú s'inscriu a una activitat "
        "i entra en llista d'espera."),
    'EMAIL_ENROLLMENT_REMINDER': (
        "",
        "Cos del correu de recordatori que s'envia a tothom que s'ha inscrit"
        "a una activitat mitjançant el botó per enviar el recordatori a "
        "tothom."),
    'EMAIL_ENROLLMENT_REMINDER_SUBJECT': (
        "Recordatori d'inscripció a l'activitat: {}",
        "Assumpte del correu de recordatori que s'envia a tothom que s'ha "
        "inscrita una activitat mitjançant el botó per enviar el recordatori "
        "a tothom."),
    'EMAIL_SIGNUP_WELCOME_SUBJECT': (
        "Nou compte creat a Coòpolis",
        "Assumpte del missatge de benvinguda que s'envia al crear un compte "
        "nou."),
    'EMAIL_SIGNUP_WELCOME': (
        "Benvingut/da a Coòpolis!<br />"
        "<br />"
        "<em>Estàs rebent aquest correu perquè s'ha completat un registre a la"
        " plataforma serveis.bcn.coop.<br />"
        "Si aquest registre no l'has fet tu o cap altra persona amb qui "
        "comparteixis aquest compte, ignora aquest"
        "correu o avisa'ns per tal que l'eliminem de la base de dades."
        "</em><br />"
        "<br />"
        "Amb el teu compte pots:<br />"
        "- Inscriure't a les sessions formatives, que trobaràs "
        "<a href=\"https://serveis.bcn.coop/program/\">aquí</a>.<br />"
        "- Si esteu iniciant o teniu en marxa un projecte cooperatiu, podeu "
        "<a href=\"https://serveis.bcn.coop/project/new/\">sol·licitar un "
        "acompanyament</a>.<br />"
        "- Consultar o editar les dades del teu perfil i recuperar la "
        "contrassenya. Més informació a "
        "<a href=\"https://serveis.bcn.coop\">serveis.bcn.coop</a>.<br />"
        "<br />"
        "L'equip de Coòpolis.<br />"
        "<a href=\"https://bcn.coop\">bcn.coop</a>",
        "Missatge de benvinguda que s'envia quan algú crea un compte."),
    'EMAIL_ADDED_TO_PROJECT_SUBJECT': (
        "Has estat afegit com a participant del projecte {}",
        "Assumpte del missatge de notificació d'haver estat afegit a un "
        "projecte."),
    'EMAIL_ADDED_TO_PROJECT': (
        "Has estat afegit com a participant al projecte acompanyat per "
        "Coòpolis:<br />"
        "{}<br />"
        "<br />"
        "Per veure i modificar la fitxa del vostre projecte, accedeix a "
        "<a href=\"https://serveis.bcn.coop/project/info/\">l'apartat "
        "Projectes</a> de la plataforma de Coòpolis amb el"
        "teu e-mail i contrasenya.<br />"
        "Si necessites la contrasenya, trobaràs l'opció per fer-ho a "
        "<a href=\"https://serveis.bcn.coop\">serveis.bcn.coop</a>.<br />"
        "<br />"
        "L'equip de Coòpolis.<br />"
        "<a href=\"https://bcn.coop\">bcn.coop</a>",
        "Missatge de notificació d'haver estat afegit a un projecte."),
    'MAIL_PASSWORD_RESET_SUBJECT': (
        "Reinici de contrasenya a serveis.bcn.coop",
        "Mail enviat quan es reinicia la contrassenya: assumpte."),
    'MAIL_PASSWORD_RESET': (
        "Has rebut aquest correu perquè hi ha hagut una sol·licitud de reinici"
        " de contrasenya del teu compte a serveis.bcn.coop.<br /><br />Si has "
        "fet tu la sol·licitud, si us plau obre el següent enllaç i escull una"
        " contrasenya nova: (password_reset_url)<br />Si no has fet tu la "
        "sol·licitud, senzillament ignora aquest correu.<br /><br />El teu "
        "nom d'usuari, en cas que l'hagis oblidat: (username)<br /><br />"
        "Gràcies per fer servir la nostra plataforma,<br />L'equip de "
        "Coòpolis",
        "Mail enviat quan es reinicia la contrassenya: cos. Ha d'incloure en "
        "algun lloc (username) i (password_reset_url) per poder mostrar el "
        "link i el nom d'usuari."),
    # Configuration
    'EMAIL_FROM_ENROLLMENTS': (
        'formacio@bcn.coop',
        "És el remitent del correu que rep la gent a l'inscriure's a una "
        "sessió. Quan s'envia un recordatori a tothom inscrit a una sessió, "
        "s'envia a aquest compte i posa en còpia oculta els correus de la "
        "gent."),
    'EMAIL_FROM_PROJECTS': (
        'suport@bcn.coop',
        "Quan algú sol·licita un acompanyament es genera un correu per "
        "notificar-ho a l'equip, que s'envia a aquest compte. Aquest camp, a "
        "diferència dels altres, permet indicar diversos comptes, separant-los"
        " per comes."),
    'EMAIL_TO_DEBUG': (
        'p.picornell@gmail.com', 'Correu per fer tests del codi.'),
    'PROJECT_NAME': ("Ateneu", "Nom curt de l'ateneu."),
    'PROJECT_FULL_NAME': (
        "Ateneu cooperatiu",
        "Nom llarg, p.ex.: 'Coòpolis. Ateneu cooperatiu de Barcelona'. També "
        "hi podeu posar el mateix que al nom curt, si voleu."),
    'PROJECT_CONTACT_URL': (
        "https://bcn.coop/contacte/",
        "Enllaç a la pàgina de contacte de l'ateneu, apareix a peu de "
        "pàgina."),
    'PROJECT_LEGAL_URL': (
        "https://bcn.coop/avis-legal-i-proteccio-de-dades/",
        "Enllaç a la pàgina de les condicions legals de l'ateneu. Apareix a: "
        "missatge d'acceptar cookies, peu de pàgina, i al text d'acceptació "
        "de condicions legals del formulari d'alta."),
    'PROJECT_WEBSITE_URL': (
        "https://bcn.coop",
        "Enllaç a la pàgina principal de l'ateneu. Apareix al menú "
        "principal."),
    'CONTACT_PHONE_NUMBER': (
        "93 432 00 63",
        "Apareix al correu que s'envia a la gent que s'inscriu a activitats, "
        "perquè sàpiguen on contactar si tenen dubtes. De la mateixa manera "
        "apareix al correu que s'envia quan envieu un recordatori a tota la "
        "gent inscrita a una sessió."),
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
        "coopolis@bcn.coop",
        "Apareix al correu que s'envia a la persona que s'ha inscrit a una "
        "sessió (i al de recordatori que s'enviamassivament des de l'admin) "
        "per indicar que si tenen dubtes, escriguin a aquest correu."),
    'ATTENDEE_LIST_FOOTER_IMG': (
        "https://s3.eu-central-1.wasabisys.com/ateneus-coopolis/local"
        "/peu_signatures_pdf.png",
        "URL de l'imatge pel peu de pàgina del llistat d'assistència."),
}
CONSTANCE_CONFIG_FIELDSETS = {
    'Configuració': (
        'PROJECT_NAME', 'PROJECT_FULL_NAME', 'ENABLE_ROOM_RESERVATIONS_MODULE',
        'ENABLE_COFUNDED_OPTIONS', 'ENABLE_STAGE_SUBTYPES',
        'PROJECT_WEBSITE_URL', 'PROJECT_LEGAL_URL', 'PROJECT_CONTACT_URL',
        'CONTACT_PHONE_NUMBER', 'CONTACT_EMAIL', 'EMAIL_TO_DEBUG',
        'EMAIL_FROM_ENROLLMENTS', 'EMAIL_FROM_PROJECTS',
        'PROJECT_FACEBOOK_URL', 'PROJECT_TWITTER_URL', 'PROJECT_INSTAGRAM_URL'
    ),
    'Correus': (
        'EMAIL_NEW_PROJECT_SUBJECT', 'EMAIL_NEW_PROJECT',
        'EMAIL_ENROLLMENT_CONFIRMATION_SUBJECT',
        'EMAIL_ENROLLMENT_CONFIRMATION',
        'EMAIL_ENROLLMENT_WAITING_LIST_SUBJECT',
        'EMAIL_ENROLLMENT_WAITING_LIST', 'EMAIL_ENROLLMENT_REMINDER_SUBJECT',
        'EMAIL_ENROLLMENT_REMINDER', 'EMAIL_SIGNUP_WELCOME_SUBJECT',
        'EMAIL_SIGNUP_WELCOME', 'EMAIL_ADDED_TO_PROJECT_SUBJECT',
        'EMAIL_ADDED_TO_PROJECT', 'MAIL_PASSWORD_RESET_SUBJECT',
        'MAIL_PASSWORD_RESET'
    ),
    "Apartat Portada": (
        'CONTENT_HOME_COURSES_TITLE', 'CONTENT_HOME_COURSES_TEXT',
        'CONTENT_HOME_PROJECTS_TITLE', "CONTENT_HOME_PROJECTS_TEXT",
        'CONTENT_HOME_INTRODUCTION'
    ),
    'Apartat Projectes': (
        'CONTENT_PROJECT_INTRODUCTION', 'CONTENT_PROJECT_TITLE',
        'CONTENT_PROJECT_INFO', 'CONTENT_PROJECT_NEW'
    ),
    "Apartat Formació": ('CONTENT_COURSES_INTRODUCTION',),
    "Formulari d'alta": ('CONTENT_SIGNUP_LEGAL1', 'CONTENT_SIGNUP_LEGAL2',),
    "Llistat d'assistència": ('ATTENDEE_LIST_FOOTER_IMG',),
}

# CC Courses

COURSES_LIST_VIEW_CLASS = 'apps.coopolis.views.CoopolisCoursesListView'
COURSES_CLASS_TO_ENROLL = 'coopolis.User'
COURSES_CLASSES_CAN_ENROLL = ['apps.cc_courses.models.Course']

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

SIGNUP_FORM = 'apps.coopolis.forms.MySignUpForm'

# Static texts and option fields
ADMIN_SITE_TITLE = ''
ADMIN_INDEX_TITLE = ''
AXIS_OPTIONS = (
    ('A', 'Eix A'),
    ('B', 'Eix B'),
    ('C', "Eix C"),
    ('D', 'Eix D'),
    ('E', 'Eix E'),
    ('F', 'Eix F'),
)
SUBAXIS_OPTIONS = {
    'A': {
        ('A1', "A.1 Reunions de la taula territorial"),
        ('A2', "A.2 Diagnosi entitats socials del territori"),
        ('A3', "A.3 Elaboració catàleg bones pràctiques"),
        ('A4', "A.4 Jornades per presentar experiències de bones pràctiques o "
               "jornades sectorials i/o d'interès per al territori"),
        ('A5', "A.5 Assistència a fires, actes per visibilitzar el programa"),
        ('A6', "A.6 Publicitat en mitjans de comunicació.  Web del programa"),
        ('A7', "A.7 Altres")
    },
    'B': {
        ('B1', "B.1 Accions de suport a la inserció laboral i a la creació de "
               "cooperatives i societats laborals (concursos de projectes "
               "cooperatius o altres accions)"),
        ('B2', "B.2 Tallers sensibilització o dinamització"),
        ('B3', "B.3 Acompanyament a empreses i entitats"),
        ('B4', "B.4 Altres"),
    },
    'C': {
        ('C1', "C.1 Tallers de dinamització adreçats al teixit associatiu i a "
               "empreses"),
        ('C2', "C.2 Tallers de dinamització adreçats a professionals que "
               "s'agrupen per prestar serveis de manera conjunta"),
        ('C3', "C.3 Acompanyament a mida per a la creació o transformació"),
        ('C4', "C.4 Altres"),
    },
    'D': {
        ('D1', "D.1 Accions de difusió"),
        ('D2', "D.2 Activitats de sensibilització o dinamització."),
        ('D3', "D.3 Acompanyament individualitzat"),
        ('D4', "D.4 Altres"),
    },
    'E': {
        ('E1', "E.1 Tallers a joves"),
        ('E2', "E.2 Atenció individual professorat"),
        ('E3', "E.3 Complementàries (recursos, eines, productes, publicacions "
               "sectorials pròpies )"),
        ('E4', "E.4 Altres"),
    },
    'F': {
        ('F1', "F.1 Pla d'actuació"),
        ('F2', "F.2 Tallers de creació de cooperatives o societats laborals, "
               "o transformació d'associacions, altres entitats"),
        ('F3', "F.3 Altres"),
    }
}
DISTRICTS = (
    ('CV', 'Ciutat Vella'),
    ('EX', 'Eixample'),
    ('HG', 'Horta-Guinardó'),
    ('LC', 'Les Corts'),
    ('NB', 'Nou Barris'),
    ('SA', 'Sant Andreu'),
    ('SM', 'Sant Martí'),
    ('ST', 'Sants-Montjuïc'),
    ('SS', 'Sarrià-Sant Gervasi'),
    ('GR', 'Gràcia')
)
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

# Django-Q
Q_CLUSTER = {
    "name": "ateneus-backoffice",
    "orm": "default",  # Use Django's ORM + database for broker
    "timeout": 30,
    "workers": 1,
}
