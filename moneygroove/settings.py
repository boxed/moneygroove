"""
Django settings for moneygroove project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!t=qk-o+(7(gzpuw3dlx6)z&6voglgb)(u=t6sxwcze6=avg0n"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'moneygroove.kodare.com'
]


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'whitenoise',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'iommi',
    'moneygroove',
]

MIDDLEWARE = [
    'iommi.live_edit.Middleware',
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # These needs to be after authentication middleware
    'iommi.sql_trace.Middleware',
    'iommi.profiling.Middleware',

    'moneygroove.middleware.auth_middleware',

    # needs to be last
    'iommi.middleware',
]

ROOT_URLCONF = "moneygroove.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "moneygroove.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if 'DOKKU_POSTGRES_MONEYGROOVE_NAME' in os.environ:
    ENV = 'prod'
    DOKKU_APP_NAME = 'MONEYGROOVE'

    dokku_db_conf = {
        'PORT': os.environ[f'DOKKU_POSTGRES_{DOKKU_APP_NAME}_PORT_5432_TCP_PORT'],
        'HOST': os.environ[f'DOKKU_POSTGRES_{DOKKU_APP_NAME}_PORT_5432_TCP_ADDR'],
        'USER': 'postgres',
        'PASSWORD': os.environ[f'DOKKU_POSTGRES_{DOKKU_APP_NAME}_ENV_POSTGRES_PASSWORD'],
        'NAME': DOKKU_APP_NAME.lower(),
        'ENGINE': 'django.db.backends.postgresql',
    }
else:
    ENV = 'dev'
    ALLOWED_HOSTS = []

    dokku_db_conf = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }


DATABASES = {
    'default': {
        **dokku_db_conf
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '\N{NO-BREAK SPACE}'
NUMBER_GROUPING = 3

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(Path(BASE_DIR) / 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'moneygroove.User'


if DEBUG:
    INSTALLED_APPS += [
        'django_pycharm_breakpoint',
        'okrand',
    ]

try:
    from .settings_local import *
except ImportError:
    pass
