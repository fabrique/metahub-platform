# -*- coding: utf-8 -*-
"""
Django settings for MetaHub online collection project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import environ

ROOT_DIR = environ.Path(__file__) - 4  # (/a/b/myfile.py - 3 = /)
SRC_DIR = environ.Path(__file__) - 3
APPS_DIR = environ.Path(__file__) - 2
FRONTEND_DIR = SRC_DIR.path('frontend')

env = environ.Env()

# try to load the env file if there is one
try:
    env.read_env(ROOT_DIR.file('.env'))
except FileNotFoundError:
    pass

DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
    'fabrique.vimeo',
    'fabrique.youtube',
)

# any app not starting with 'django.'
THIRD_PARTY_APPS = (

    # customize wagtail here
    'metahub.cms',

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',
    'wagtail.contrib.search_promotions',
    'wagtail.contrib.routable_page',

    'modelcluster',
    'taggit',
    'wagtailfontawesome',
    'pure_pagination',

    'webpack_loader',
    'axes',

    #for search!
    'django_elasticsearch_dsl',

    'starling',

    # API
    'corsheaders',


)

# Apps specific for this project go here.
LOCAL_APPS = (
    # Our apps
    'metahub.core',
    'metahub.menu',
    'metahub.frontend',
    'metahub.sync',
    'metahub.collection',
    'metahub.api'

    # custom apps go here
)


CORS_ALLOW_ALL_ORIGINS=True
CORS_URLS_REGEX = r'^/api/.*$'
# CORS_ORIGIN_WHITELIST = (
#     'https://127.0.0.1',
# )
CORS_ALLOW_METHODS = [
    'GET',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'wagtail.contrib.legacy.sitemiddleware.SiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    # It only formats user lockout messages and renders Axes lockout responses
    # on failed user authentication attempts from login views.
    # If you do not want Axes to override the authentication response
    # you can skip installing the middleware and use your own views.
    'axes.middleware.AxesMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

)

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

# this adds the domain name to the sites model
MIGRATION_MODULES = {
    'sites': 'contrib.sites.migrations'
}

DEBUG = env.bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['collection.metahub.de'])

FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

DATABASES = {
    'default': env.db("DJANGO_DATABASE_URL", default="postgres:///metahub"),
}
DATABASES['default']['CONN_MAX_AGE'] = None
DATABASES['default']['ATOMIC_REQUESTS'] = True

TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ = False

LANGUAGES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
]

WAGTAILADMIN_PERMITTED_LANGUAGES = LANGUAGES

LOCALE_PATHS = (
    str(APPS_DIR.path('locale')),
)

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # wagtail custom 'live' settings are available in the template
                'wagtail.contrib.settings.context_processors.settings',

                # Custom template context processors go here
            ],
        },
    },
]

STATIC_ROOT = str(ROOT_DIR('static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
    str(ROOT_DIR.path('assets')),
    str(SRC_DIR.path('frontend', 'build', 'static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'TIMEOUT': 10,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': str(ROOT_DIR('webpack-stats.json')),
        'POLL_INTERVAL': 0.1,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

FILE_UPLOAD_PERMISSIONS = 0o664

MEDIA_ROOT = str(ROOT_DIR('media'))
MEDIA_URL = '/media/'

ROOT_URLCONF = 'metahub.urls'
WSGI_APPLICATION = 'metahub.wsgi.application'


WAGTAILIMAGES_IMAGE_MODEL = 'core.metahubImage'
WAGTAIL_SITE_NAME = 'MetaHub online collection'


GOOGLE_TAG_MANAGER_ID = env.str("DJANGO_GOOGLE_TAG_MANAGER_ID", '')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Set slightly more forgiving axes defaults
AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = 1

#read this for detailed info on django_elasticsearch_dsl
#https://django-elasticsearch-dsl.readthedocs.io/en/latest/quickstart.html

# TODO this is for indexing doc content only
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}
# dynamic index name, used by indexing and searching accordingly
ES_INDEX_NAME = env.str("DJANGO_ES_INDEX_NAME", '')

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 5,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}