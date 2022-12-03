"""
Imported Packeges
"""

# By Default
from pathlib import Path

# Decouple for Hiding all Credentials
from decouple import config


# Date & Time
from datetime import timedelta

# System
import os


"""
******************************************************************************************************************
                                    Basic Settings
******************************************************************************************************************
"""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


"""
*************************************
        Secret Key & Debug
*************************************
"""


SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG")


"""
*************************************
        ALLOWED_HOSTS
*************************************
"""


ALLOWED_HOSTS = []


# *************************************
#          INSTALLED_APPS
# *************************************


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Rest Framework
    'rest_framework',

    # Authentication Token
    'rest_framework.authtoken',

    # Swagger
    'drf_yasg',

    # Simple JWT
    'rest_framework_simplejwt',

    # Black list Token - Log Out
    'rest_framework_simplejwt.token_blacklist',

    # App 9SPL
    'App9SPL.apps.App9SplConfig'
]


# *************************************
#             MIDDLEWARE
# *************************************

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Project9SPL.urls'


# *************************************
#             TEMPLATES
# *************************************


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
            ],
        },
    },
]


# *************************************
#             WSGI_APPLICATION
# *************************************

WSGI_APPLICATION = 'Project9SPL.wsgi.application'


# *************************************
#             DATABASES
# *************************************

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


"""
*************************************
            Time Zone
*************************************
"""

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


"""
*************************************
             Static Files
*************************************
"""

# ******************  Static   ******************
STATIC_ROOT = os.path.abspath(os.path.join(
    BASE_DIR, 'ProjectCLB', 'static'))

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')

]

# ******************  Media   ******************
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")


"""
*************************************
        DEFAULT_AUTO_FIELD
*************************************
"""

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


"""
******************************************************************************************************************
                                    Customs Settings
******************************************************************************************************************
"""


"""
*************************************
    Authentication Custom User Model
*************************************
"""

AUTH_USER_MODEL = "App9SPL.SystemUser"


"""
*************************************
            Rest Frame Work
*************************************
"""


REST_FRAMEWORK = {

    # Filter
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    # Globally Authentication - JWT
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # Permission Class
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


"""
*************************************
            Simple JWT
*************************************
"""

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=59),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

}


"""
*************************************
                Swagger
*************************************
"""

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'testproj.urls.swagger_info',
    'JSON_EDITOR': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
    }
}
