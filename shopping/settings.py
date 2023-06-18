"""
Django settings for shopping project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',default=False,cast=bool)

ALLOWED_HOSTS = ['13.53.47.141','gamepy.online']


# Application definition

INSTALLED_APPS = [
    'accounts',
    'category',
    'products',
    'carts',
    'orders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'whitenoise.runserver_nostatic', 
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_rename_app',
    'decouple',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shopping.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.nav_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopping.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'USER': 'gamepy2',
        'PASSWORD': config('PASSWORD'),
        'HOST':config('HOST'),
        'PORT':config('PORT'),
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

import os

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR,'static')
# ] 

# Media Files Configuration 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')





# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

 
# SMTP Configuration
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT',cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_BACKEND = config('EMAIL_BACKEND')




# SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'/

AWS_ACCESS_KEY_ID=config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME=config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME=config('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME=config('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
AWS_S3_VERITY=True
DEFAULT_FILE_STORAGE=config('DEFAULT_FILE_STORAGE')
