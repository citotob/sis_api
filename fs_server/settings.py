"""
Django settings for fs_server project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import logging
import mongoengine
#import fcm
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z-q#mm1*k40u5t)20t*-4_)t1-!%1b_cdi59t5-#i2^5mev*3d_sis'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
CORS_ALLOW_HEADERS = ('*')
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

# CORS_ORIGIN_WHITELIST = (
#    'https://survejdev-api.datasintesa.id'
#     'http://localhost:8000',
# 	 'http://localhost:8080'
# )


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

FILE_UPLOAD_PERMISSIONS = 0o644

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_mongoengine',
    'corsheaders',
    'userinfo',
    # 'sites',
    # 'Location',
    'vendor',
    'Location',
    'vendorperformance',
    # 'configparser',
    'channels',
    'userinfo.utils',
    'secrets',
    'odps',
    'check',
    'publicservice'
]


ASGI_APPLICATION = 'fs_server.routing.application'
# CHANNEL_LAYERS = {
#    'default': {
#        'BACKEND': 'channels_redis.core.RedisChannelLayer',
#        'CONFIG': {
#            "hosts": [('127.0.0.1', 6379)],
#        },
#    },
# }
# Channels
CHANNEL_LAYERS = dict(default=dict(
    BACKEND="channels.layers.InMemoryChannelLayer"))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fs_server.urls'
#AUTH_USER_MODEL = 'userinfo.userinfo'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'fs_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {'default': {
    'ENGINE': '', },
}

# DATABASES = {
#        'default': {
#            'ENGINE': 'djongo',
#            'NAME': 'monev',
#        }
#    }
#DATABASES = {}

#SESSION_ENGINE = 'mongoengine.django.sessions'

MONGO_NAME = 'sis'
#MONGO_DATABASE_HOST = 'mongodb://userSIS:usercaptive@165.22.58.39:27017/sis'
MONGO_DATABASE_HOST = 'mongodb://userSIS:SISpassword2020#@116.66.206.230:27017/sis'
# MONGO_DATABASE_HOST = 'mongodb://userSIS:SISpassword2020#@103.129.220.176:27017/sis'
mongoengine.connect(MONGO_NAME, host=MONGO_DATABASE_HOST)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher'
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

FCM_DJANGO_SETTINGS = "AAAAcKWkQqY:APA91bFPIabxvd3aX3qksodzAjJP8wOs4mS0rhiM8OZ8s9njjfPwzNOGkYQvdCehTFZXhQ5eEpwDgsjnG_ZQyWpUJnZkWmhR_C7_v4VNrdDNaoCb6bc-1ZSZhwxU8fI1ZosoHflqASc4"

#DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

APPEND_SLASH = True

# configure logging
"""
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        #'console': {
        #    'format': '%(name)-12s %(levelname)-8s %(message)s'
        #},
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'sis.log')
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'daphne': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG'
        },
    }
})
"""

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-4cf3bba899c0ad2082a11990061c2be4'
MAILGUN_SERVER_NAME = 'dev.datasintesa.id'

EMAIL_ADMIN = 'SIS-INFO<info.sisbakti.id>'

URL_LOGIN = 'https://teksas.devlabs.id/login'
URL_REGISTER = 'https://teksas.devlabs.id/register'
URL_MEDIA = 'https://teksas-api.devlabs.id/media'
URL_RESETPASSWORD = 'https://teksas.devlabs.id/resetpassword'

# RECAPTCHA_SITE_KEY = "6LfRt-kZAAAAAK08jXgSumEsBGOhWjI-yY8kcvyE"
# RECAPTCHA_SECRET_KEY = "6LfRt-kZAAAAABgVg-g4FUIOEHAIv8HH8hX4agut"
RECAPTCHA_SITE_KEY = "6LeGOj4bAAAAAPjz5gczQT397UGwjS4P7lN16Bou"
RECAPTCHA_SECRET_KEY = "6LeGOj4bAAAAAM18ogVjoZHsPZvqduJ-h4RS1bAA"
