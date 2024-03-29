import os

import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'wagtail.contrib.forms',
    'wagtail.contrib.frontend_cache',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',

    'tmknorg.core',
    'tmknorg.documents',
    'tmknorg.home',
    'tmknorg.blog',
    'tmknorg.images',
    'tmknorg.photostream',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_referrer_policy.middleware.ReferrerPolicyMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'tmknorg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'tmknorg.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600),
}


# Cache
# https://docs.djangoproject.com/en/2.0/topics/cache/

if 'REDIS_URL' in os.environ:
    # https://niwinz.github.io/django-redis/latest/
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ['REDIS_URL'],
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# http://whitenoise.evans.io/en/stable/django.html#add-compression-and-caching-support

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


# S3 media

if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
    INSTALLED_APPS.append('storages')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_FILE_OVERWRITE = False
    if 'AWS_S3_CUSTOM_DOMAIN' in os.environ:
        AWS_S3_CUSTOM_DOMAIN = os.environ['AWS_S3_CUSTOM_DOMAIN']


# Security settings

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = (
    os.environ.get('SECURE_SSL_REDIRECT', 'true').strip().lower() == 'true'
)

SECURE_BROWSER_XSS_FILTER = (
    os.environ.get('SECURE_BROWSER_XSS_FILTER',
                   'true').strip().lower() == 'true'
)

SECURE_CONTENT_TYPE_NOSNIFF = (
    os.environ.get('SECURE_CONTENT_TYPE_NOSNIFF',
                   'true').strip().lower() == 'true'
)

SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 0))

REFERRER_POLICY = 'same-origin'


# Basic auth
# https://gitlab.com/tmkn/django-basic-auth-ip-whitelist

if os.environ.get('ENABLE_BASIC_AUTH', '').lower().strip() == 'true':
    MIDDLEWARE += [
        'baipw.middleware.BasicAuthIPWhitelistMiddleware'
    ]
    if 'BASIC_AUTH_LOGIN' in os.environ:
        BASIC_AUTH_LOGIN = os.environ['BASIC_AUTH_LOGIN']
    if 'BASIC_AUTH_PASSWORD' in os.environ:
        BASIC_AUTH_PASSWORD = os.environ['BASIC_AUTH_PASSWORD']
    if 'BASIC_AUTH_WHITELISTED_IP_NETWORKS' in os.environ:
        BASIC_AUTH_WHITELISTED_IP_NETWORKS = (
            os.environ['BASIC_AUTH_WHITELISTED_IP_NETWORKS']
        )
    if 'BASIC_AUTH_WHITELISTED_HTTP_HOSTS' in os.environ:
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS = (
            os.environ['BASIC_AUTH_WHITELISTED_HTTP_HOSTS']
        )


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'wagtail': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'tmknorg': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    },
}

# Front-end cache

if 'FRONTEND_CACHE_CONTROL_S_MAX_AGE' in os.environ:
    FRONTEND_CACHE_CONTROL_S_MAX_AGE = (
        os.environ['FRONTEND_CACHE_CONTROL_S_MAX_AGE']
    )

if 'FRONTEND_CACHE_CLOUDFLARE_TOKEN' in os.environ:
    WAGTAILFRONTENDCACHE = {
        'cloudflare': {
            'BACKEND': (
                'wagtail.contrib.frontend_cache.backends.CloudflareBackend'
            ),
            'EMAIL': os.environ['FRONTEND_CACHE_CLOUDFLARE_EMAIL'],
            'TOKEN': os.environ['FRONTEND_CACHE_CLOUDFLARE_TOKEN'],
            'ZONEID': os.environ['FRONTEND_CACHE_CLOUDFLARE_ZONEID'],
        },
    }

# Wagtail settings
WAGTAIL_SITE_NAME = 'tmkn'

WAGTAILIMAGES_IMAGE_MODEL = 'images.CustomImage'

WAGTAILDOCS_DOCUMENT_MODEL = 'documents.CustomDocument'
