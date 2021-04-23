# -*- coding: utf-8 -*-
"""
Production Configurations

- Use sentry for error logging
"""
from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")

# raven sentry client
# See https://docs.getsentry.com/hosted/clients/python/integrations/django/
INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

RAVEN_CONFIG = {
    'dsn': env.str('DJANGO_SENTRY_DSN', ''),
}

SECURITY_MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
)

RAVEN_MIDDLEWARE = ('raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',)
MIDDLEWARE = SECURITY_MIDDLEWARE + \
             RAVEN_MIDDLEWARE + MIDDLEWARE 

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['collection.metahub.de'])
# END SITE CONFIGURATION

# INSTALLED_APPS += ("gunicorn", )

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader',
     ['django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db("DJANGO_DATABASE_URL")

# Custom Admin URL, use {% url 'admin:index' %}
ADMIN_URL = env('DJANGO_ADMIN_URL')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        'KEY_PREFIX': env.str('DJANGO_CACHE_KEY_PREFIX', ''),
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # sentry does logging
}

WEBPACK_LOADER['DEFAULT']['CACHE'] = True

# Your production stuff: Below this line define 3rd party library settings
