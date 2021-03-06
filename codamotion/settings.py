"""
Django settings for codamotion project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os 
import urllib.parse 
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG'))) if os.environ.get('DEBUG') else True

# SECURITY WARNING: keep the secret key used in production secret!
if not DEBUG:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = '(vun=w5id#m!0(0d4^#!y1w05crrxyw^%1zdrjg5-bgig+vr&%'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'codamotion.herokuapp.com', 'codamotion.com', os.environ.get('ALLOWED_HOSTS')]
INTERNAL_IPS = ['localhost', '127.0.0.1']

# Captcha Secret Keys
if os.environ.get('RECAPTCHA_PUBLIC_KEY') and os.environ.get('RECAPTCHA_PRIVATE_KEY'):
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
elif DEBUG:
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'website.apps.WebsiteConfig',

    'modelcluster',
    'captcha',
    'storages',

    'widget_tweaks',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'codamotion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'codamotion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
if not DEBUG:
    if os.environ.get('AZURE'):
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('AZURE_DB_NAME'),
            'HOST': os.environ.get('AZURE_DB_HOST') + '.postgres.database.azure.com',
            'PORT': 5432,
            'USER': os.environ.get('AZURE_DB_USER') + "@" + os.environ.get('AZURE_DB_HOST'),
            'PASSWORD': urllib.parse.unquote(os.environ.get('AZURE_DB_PW')),
        }
    else:
        import dj_database_url
        DATABASES['default'] = dj_database_url.config()

# Custom user auth
AUTH_USER_MODEL = 'website.User'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

if not DEBUG and os.environ.get('AZURE_STORAGE_ACCOUNT_NAME'):
    # The below is not currently in use due to the Azure Storage not being 
    # set up on the Production server. May come in hand if/when that is set up.
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY')
    AZURE_CONTAINER = os.environ.get('AZURE_STORAGE_CONTAINER')
    AZURE_LOCATION = os.environ.get('AZURE_STORAGE_LOCATION') or "" 
    AZURE_ENDPOINT_SUFFIX = os.environ.get('AZURE_STORAGE_ENDPOINT_SUFFIX') or 'core.windows.net'
    AZURE_CUSTOM_DOMAIN = os.environ.get('AZURE_STORAGE_CUSTOM_DOMAIN') or None 
    AZURE_TOKEN_CREDENTIAL = os.environ.get('AZURE_STORAGE_TOKEN') or None 
else:    
    MEDIA_URL = '/media/'