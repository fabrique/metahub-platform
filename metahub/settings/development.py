# -*- coding: utf-8 -*-
"""
Development settings

- Run in Debug mode
- Use file backend for emails
- Set allowed_hosts to localhost
- Set dummy cache
- Setup logging to console
"""
import socket

from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
# DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# ALLOWED HOSTS
# ------------------------------------------------------------------------------
hostname = socket.gethostname()  # your computer name, so mbdev###

# get a list of all local ips
try:
    local_addresses = [local[4][0] for local in socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)]
except socket.gaierror:
    local_addresses = []
    print("Local IP addresses could not be determined")

default_hosts = [hostname, 'localhost', '0.0.0.0', '127.0.0.1'] + local_addresses
ALLOWED_HOSTS = default_hosts + env.list('DJANGO_ALLOWED_HOSTS', default=[])

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
# For staging/production, another randomly generated key should be in the corresponding .env
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!6hj)h@2k7^d0igrp4vqi)%@-c8fqi=5r49m(-4r)nh=x!#j_mq')

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.filebased.EmailBackend')
EMAIL_FILE_PATH = str(ROOT_DIR.path('mail/'))

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


INSTALLED_APPS += (
    'wagtail.contrib.styleguide',
)


# Add Fabrique developer tools
INSTALLED_APPS = (
    'devtools',
) + INSTALLED_APPS

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# make rosetta work without cache
# ROSETTA_STORAGE_CLASS = 'rosetta.storage.SessionRosettaStorage'

# Your local stuff: Below this line define 3rd party library settings

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'metahub': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

DEPLOY_CONFIGURATION = {
    'default': {
        'git_url': '',
        'project_name': 'metahub',
        'remote_user': 'webdev',
        'remote_host': '87.233.196.130',
        'skip_deploy_phases': ['reload-nginx'],
    },
    'production': {
        'branch': 'master',
        'project_dir': '/data/www/metahub/production',
        'src_dir': '/data/www/metahub/production/src',
        'venv_dir': '/data/www/metahub/production/venv',
        'supervisor_name': 'metahub-production',
    },
    'staging': {
        'branch': 'master',
        'project_dir': '/data/www/metahub/staging',
        'src_dir': '/data/www/metahub/staging/src',
        'venv_dir': '/data/www/metahub/staging/venv',
        'supervisor_name': 'metahub-staging',
        'remote_user': 'webdev',
        'remote_host': 'metahub.fabriquehq.nl', #todo change when domain exists
    },
}


