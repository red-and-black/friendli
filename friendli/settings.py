"""
Django settings for friendli project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Specify whether this is a development or production instance.
environment = os.environ['FRIENDLI_ENVIRONMENT']
if environment not in ['production', 'development']:
    msg = "The environment must be either 'production' or 'development'."
    raise Exception(msg)
IS_PRODUCTION_INSTANCE = (environment == 'production')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['FRIENDLI_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if IS_PRODUCTION_INSTANCE else True

ALLOWED_HOSTS = ['.friendli.io'] if IS_PRODUCTION_INSTANCE else []


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'behaviour',
    'common',
    'conferences',
    'conversations',
    'dash',
    'friendli',  # TODO: Remove this. It's a hack so that base.html is found.
    'meetups',
    'pages',
    'profiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'friendli.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'friendli.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'conferences.context_processors.conference_name',
                'conversations.context_processors.unread_messages_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'friendli.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['FRIENDLI_DATABASE_NAME'],
        'PASSWORD': os.environ['FRIENDLI_DATABASE_PASSWORD'],
        'USER': os.environ['FRIENDLI_DATABASE_USER'],
    }
}
if IS_PRODUCTION_INSTANCE:
    DATABASES['default']['HOST'] = os.environ['FRIENDLI_DATABASE_HOST']
else:
    DATABASES['default']['HOST'] = 'localhost'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'friendli', 'static'),)

if IS_PRODUCTION_INSTANCE:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
    STATIC_ROOT = '/home/friendli/static/'


# Dates and times
# https://docs.djangoproject.com/en/3.0/ref/settings/#date-format

DATE_INPUT_FORMATS = ['%d/%m/%y', '%d/%m/%Y']
TIME_INPUT_FORMATS = ['%I:%M%p', '%H:%M', '%I %p', '%I:%M %p', '%I%p']

# Authentication
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth

LOGIN_URL = 'login'


# Email
# https://docs.djangoproject.com/en/3.0/ref/settings/#email-backend

# TODO: Dehardcode ADMINS.
ADMINS = [
    ('Keira', 'keira@keirapaterson.com'),
    ('Sky', 'sky@skychristensen.com'),
]
# TODO: Change the email to noreply@friendli.io, but at the moment this will
# stop email from being sent, so fix the server first.
DEFAULT_FROM_EMAIL = 'friendli@friendli.io'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
if IS_PRODUCTION_INSTANCE:
    EMAIL_BACKEND = 'friendli.backends.LoggingSmtpEmailBackend'
else:
    EMAIL_BACKEND = 'friendli.backends.LoggingFileBasedEmailBackend'
    EMAIL_FILE_PATH = '/tmp/friendli/emails'
    os.makedirs(EMAIL_FILE_PATH, exist_ok=True)


# Logging
# https://docs.djangoproject.com/en/3.0/ref/settings/#logging

if IS_PRODUCTION_INSTANCE:
    log_dir = '/home/friendli/logs/'
else:
    log_dir = '/tmp/friendli/logs/'
os.makedirs(log_dir, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'requests': {
            'format': '[%(asctime)s] -- %(message)s',
        },
        'mail': {
            'format': '[%(asctime)s] %(levelname)s -- %(message)s',
        },
    },
    'handlers': {
        'all_requests': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_dir, 'requests.log'),
            'formatter': 'requests',
        },
        'mail': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_dir, 'mail.log'),
            'formatter': 'mail',
        },
    },
    'loggers': {
        'django.all_requests': {
            'handlers': ['all_requests'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.mail': {
            'handlers': ['mail'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security
if IS_PRODUCTION_INSTANCE:
    CSRF_COOKIE_SECURE = True
    LANGUAGE_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

# Channels.
ASGI_APPLICATION = "friendli.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
