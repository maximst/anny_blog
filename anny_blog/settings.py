# Django settings for anny_blog project.

import os

def autopath(*dirname):
    return os.path.join(os.path.split(os.path.dirname(__file__)\
                                    .replace('\\', '/'))[0], *dirname)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

HOSTNAME = 'follow-chic.com'

ADMINS = (
    ('Anny', 'Annymodel@yandex.ua'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = autopath('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = autopath('staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    autopath('static'),
    autopath('media'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.MySocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'anny_blog.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'anny_blog.wsgi.application'

TEMPLATE_DIRS = (
    autopath('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'south',
    'voting',
    'taggit',
    'social.apps.django_app.default',
    'coffeescript',
    'sorl.thumbnail',
    'linkexchange_django',
    'sape.django',
    'supercaptcha',
    'compressor',

    'blog',
    'tag',
    'core',
    'user_profile',
    'radio',
    'poll',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
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
    }
}



TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'linkexchange_django.context_processors.linkexchange',
    'sape.django.context_processors.sape',
    'context_processors.core.core',
)
CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS

LOGIN_URL = '/accounts/login/'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

STUPIDITY_LEVELS = (
    (0, '1'),
    (1, '2'),
    (2, '3'),
    (3, '4'),
)

MENU_ITEMS = (
    ('blog', 'Blog'),
)

LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_ERROR_URL    = '/accounts/login-error/'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'user_profile.pipeline.set_user_profile'
)

SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

COFFEESCRIPT_ROOT = autopath('static')
LINKEXCHANGE_CONFIG = autopath('anny_blog', 'linkexchange.cfg')
SAPE_DATABASE = autopath('sape')
SAPE_USER = '1ace11f022c3a648b3cc382788c589cd'
SAPE_HOST = HOSTNAME

COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
)

THUMBNAIL_QUALITY = 80

AVATAR_SIZE = (100, 100)

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * (1024 * 1024)

CACHE_TIMEOUT = 0 #60 * 15

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'TIMEOUT': CACHE_TIMEOUT,
        'KEY_PREFIX': '',
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    },
}

SOUTH_MIGRATION_MODULES = {
    'default': 'social.apps.django_app.default.south_migrations'
}

try:
    from .local_settings import *
except ImportError:
    pass

