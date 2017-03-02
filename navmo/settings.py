"""
Django settings for navmo project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-pvvmb(2t%tfvxhkqftpt%u4&bihrow!+ic9&$3k42yi_lmtg='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.116']#'139.59.17.151','mpenavmo.com','www.mpenavmo.com','www.mpenavmo.com/static','mpenavmo.com/static']
#ALLOWED_HOSTS = [u'127.0.0.1']#'139.59.17.151','mpenavmo.com','www.mpenavmo.com','www.mpenavmo.com/static','mpenavmo.com/static']
#ALLOWED_HOSTS = ['192.168.0.105']#'139.59.17.151','mpenavmo.com','www.mpenavmo.com','www.mpenavmo.com/static','mpenavmo.com/static']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'register',
    'otp',
    'payment',
    'forgot_password',
    'admit_card',
    'photo_gallery',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'navmo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['navmo/templates'],
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

WSGI_APPLICATION = 'navmo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
#  }

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'navmo',
        'USER': 'root',
        'PASSWORD': 'Localcart@999123',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

import django.contrib.auth
django.contrib.auth.LOGIN_URL = '/login'
# Application definition

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
import os
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = "media/"
# MEDIA_ROOT = os.path.join(BASE_DIR,"/media/")
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreplycodenicely@gmail.com'
EMAIL_HOST_PASSWORD = 'xthbbcjthowlnrky'
EMAIL_PORT = 587
EMAIL_USE_TLS = True