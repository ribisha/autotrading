
from pathlib import Path
import os
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-%z59mk(s%lxk35dixc=l6!j)4an7@#b43$k&e830f$*mbrg0wq'
DEBUG = True
ALLOWED_HOSTS = ['*']  

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'client',
    'master',
    'staff',
    'debug',
    'authentication',
    'finance',
    'django_template_maths',
    'django_celery_beat',
    'django_celery_results',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'investou.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'investou.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


JAZZMIN_UI_TWEAKS = {
    "theme": "simplex",
}
JAZZMIN_SETTINGS = {
    "site_title": "Investou",
    "site_header": "Investou",
    "site_brand": "Investou",
    "site_icon": "images/favicon.png",
   
}


ALLOWED_HOSTS = ['127.0.0.1', 'apiconnect.angelbroking.com']

# CELERY_BEAT_SCHEDULE = {
#     'update-data-periodically-task': {
#         'task': 'investou.tasks.update_data_periodically',
#         'schedule': 60,  # Interval in seconds (e.g., 1 minute)
#         'args': (),
#     },
# }


#CELERY SETTINGS
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'


#CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# Celery configuration

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# username=ribi
# api_key = 'rCE2dY2L'
# client_id = 'R56578152'
# pin = '1995'
# qr_value = 'RDN4BJ2YR676SJQ4IHRYKEQASY'



# username=nazimm
# Api key : rJIPyddu 
# Client ID : IIRA97953
# PIN: 9995
# TOTP QR :BIVBJ7FSXYZW5MG3AO7YOGISBY

#username=anju
#  Api key= jTdFKiQb
#  Client ID= A57045510
#  qr_value= TZEX5Y7LW4LW2SZPTVMFHTYTQU
#  pin= 8075