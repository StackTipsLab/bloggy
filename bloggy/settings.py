"""
Django settings for bloggy project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production

# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

# enable special cases like tag manager enabled in dev mode. Used to override the default DEBUG behaviour
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1, localhost").split(",")
INTERNAL_IPS = ['127.0.0.1']

SITE_URL = os.getenv("SITE_URL")

# Application definition
INSTALLED_APPS = [
    'bloggy',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # sitemap
    'django.contrib.sitemaps',

    # 'tinymce',
    'widget_tweaks',
    'django_summernote',
    'whitenoise.runserver_nostatic',

    'rest_framework',
    'bloggy_api',
    'mail_templated',  # Used for templated email https://github.com/artemrizhov/django-mail-templated
    'storages',
    'debug_toolbar',  # dev only

    'hitcount',
    'colorfield'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'bloggy.middleware.wp_redirect.OldUrlRedirectMiddleware',  # redirect for old wp site urls
    'bloggy.middleware.slash_middleware.AppendOrRemoveSlashMiddleware',  # Remove slash from url

    # Cache
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # Cache

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Social login
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'bloggy.middleware.page_not_found.PageNotFoundMiddleware',  # new articles mismatch url redirect
]

ROOT_URLCONF = 'bloggy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': os.path.join(BASE_DIR, '/bloggy/templates'),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bloggy.context_processors.seo_attrs',
                'bloggy.context_processors.app_settings',

                # Social login
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'bloggy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {'charset': 'utf8mb4', 'use_unicode': True},
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

USE_SPACES = os.getenv('USE_SPACES') == 'True'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = f'https://{os.getenv("AWS_S3_ENDPOINT_URL")}'

if USE_SPACES:
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'{os.getenv("ASSETS_DOMAIN")}/static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    MEDIA_URL = f'/media/'
    DEFAULT_FILE_STORAGE = 'bloggy.storage_backends.PublicMediaStorage'
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'bloggy.storage_backends.PrivateMediaStorage'

    AWS_S3_CUSTOM_DOMAIN = 'media.stacktips.com'


else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'bloggy/')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'code',
    'toolbar': 'code',
}

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'bloggy.MyUser'
AUTH_USER_DEFAULT_GROUP = 'bloggy-members'

SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'width': '1000',
        'height': '720',
        'styleTags': [
            'p',
            {
                'title': 'Blockquote',
                'tag': 'blockquote',
                'className': 'blockquote',
                'value': 'blockquote'
            },
            {
                'title': 'Code Block',
                'tag': 'pre',
                'className': 'prettyprint lang-java',
                'value': 'pre'
            },
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        ],

        'airMode': False,
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'code']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    },

    'codemirror': {
        'mode': 'htmlmixed',
        'lineNumbers': 'true',
        'theme': 'monokai',
    },

    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
    ),
    'attachment_require_authentication': True,
    'attachment_upload_to': 'uploads/summernote',
    'attachment_model': 'bloggy.Media',
    'attachment_absolute_uri': False

}

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

SITE_TITLE = "StackTips"
SITE_DESCRIPTION = "Free programming tutorials, how-to guides, code snippets on various tech subjects"
SITE_LOGO = "https://media.stacktips.com/static/media/logo.png"

# Social login
AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

GOOGLE_RECAPTHCA_SECRET_KEY = os.getenv('GOOGLE_RECAPTHCA_SECRET_KEY')
GOOGLE_RECAPTHCA_TOKEN_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'bloggy_api.pagination.CustomPaginatedResponse',
    'PAGE_SIZE': 30,

    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
}

# CACHE CONFIG
CACHE_TTL = 60 * 15
CACHE_MIDDLEWARE_ALIAS = 'default'  # which cache alias to use
CACHE_MIDDLEWARE_SECONDS = CACHE_TTL  # number of seconds to cache a page for (TTL)
CACHE_MIDDLEWARE_KEY_PREFIX = ''  # should be used if the cache is shared across multiple sites that use the same Django instance

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }, 'redis': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379',
            "KEY_PREFIX": "bloggy"
        },
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': os.getenv("MEMCACHIER_SERVERS", "127.0.0.1:11211"),
            "OPTIONS": {
                "binary": True,
                # 'username': os.getenv("MEMCACHIER_USERNAME", ""),
                # 'password': os.getenv("MEMCACHIER_PASSWORD", ""),
                "behaviors": {
                    "ketama": True,
                },
            },
        }
    }

ASSETS_DOMAIN = os.getenv("ASSETS_DOMAIN", "https://media.stacktips.com")

# Django HitCount
HITCOUNT_KEEP_HIT_ACTIVE = {'days': 0}
HITCOUNT_KEEP_HIT_IN_DATABASE = {'days': 77}
HITCOUNT_HITS_PER_IP_LIMIT = 0

# Shotcode
SHORTCODES_YOUTUBE_JQUERY = False

# SEO related
PING_INDEX_NOW_POST_UPDATE = os.getenv("PING_INDEX_NOW_POST_UPDATE", True)
PING_GOOGLE_POST_UPDATE = os.getenv("PING_GOOGLE_POST_UPDATE", True)
INDEX_NOW_API_KEY = os.getenv("INDEX_NOW_API_KEY", "220764bdee4b4ff297c588217aaaafa3")

# Email configs
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'hello.stacktips@gmail.com')
EMAIL_FILE_PATH = os.getenv('EMAIL_FILE_PATH', os.path.join(BASE_DIR, 'test-mails'))
