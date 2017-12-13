import os
import sys

DEBUG = False

QA_SERVER = False  # triggers minor UI changes

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Yaniv Mirel', 'yanivmirel@gmail.com'),
)

EMAIL_SUBJECT_PREFIX = '[OpenComm] '
FROM_EMAIL = "noreply@opencomm.org.il"
HOST_URL = "http://localhost:8000"

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'opencomm',
        'USER': 'opencomm',
        'PASSWORD': 'opencomm',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

FILE_UPLOAD_PERMISSIONS = 0o664

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

ALLOWED_HOSTS = []

TIME_ZONE = 'Asia/Jerusalem'
LANGUAGE_CODE = 'he'
USE_I18N = True
USE_L10N = True
USE_TZ = True

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    LANGUAGE_CODE = 'en'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'ocd', 'locale'),
)

UPLOAD_PATH = os.path.join(BASE_DIR, 'uploads')

UPLOAD_ALLOWED_EXTS = [
    'pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx', 'csv',
    'jpg', 'jpeg', 'gif', 'png', 'tiff', 'ppt', 'pptx',
    'rtf', 'mp3', 'wav', 'flac', 'm4a', 'wma', 'aac',
    'fla', 'mp4', 'mov', 'avi', 'wmv',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

SECRET_KEY = '!9cmmoa+#@=9o33n+wf+kf)))u6!0b)z(l-h-sq4sk*jv9&^6*'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ocd.urls'

WSGI_APPLICATION = 'ocd.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ocd.context_processors.analytics',
                'ocd.context_processors.smart_404',
            ],
        },
    },
]

INSTALLED_APPS = [
    'communities.apps.CommunitiesConfig',
    'issues.apps.IssuesConfig',
    'meetings.apps.MeetingsConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_rq',
    'django_nose',
    'django_extensions',
    'taggit',
    # 'haystack',
    'oc_util',
]

AUTH_USER_MODEL = 'users.OCUser'

HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'ocd.custom_whoosh_backend.MyWhooshEngine',
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_CUSTOM_HIGHLIGHTER = 'ocd.custom_highlighting.MyHighlighter'
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "login"
LOGOUT_URL = "logout"

FORMAT_MODULE_PATH = "ocd.formats"
DATE_FORMAT_OCSHORTDATE = "j.n"
DATE_FORMAT_OCSHORTTIME = "H:i"

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

SESSION_REMEMBER_DAYS = 45
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

REDIS = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
        'SCHEME': 'redis://'
    }
}

gettext = lambda s: s

OPENCOMMUNITY_ANALYTICS = {
    'ga': {
        'id': 'UA-00000000-0',
        'url': 'domain.com'
    }
}

OPENCOMMUNITY_DEFAULT_CONFIDENTIAL_REASONS = [
    gettext('Privacy'),
    gettext('Commercial'),
    gettext('Security'),
    gettext('Legal')
]

OPENCOMMUNITY_ASYNC_NOTIFICATIONS = False

version_file = os.path.join(STATIC_ROOT, 'version.txt')
if os.path.exists(version_file):
    with open(version_file) as f:
        OPENCOMMUNITY_VERSION = f.read()
else:
    OPENCOMMUNITY_VERSION = None

QUEUE_NAME = 'default'

try:
    from .local_settings import *
except ImportError:
    pass

RQ_QUEUES = {
    QUEUE_NAME: REDIS['default'],
}
