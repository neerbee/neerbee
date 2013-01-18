# Django settings for neerbee project.
import os
from urlparse import urlparse

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# use sqlite only if on dev machine
if not os.environ.get('MONGOHQ_URL'):
    DATABASES = {
                'default': {
                            'ENGINE': 'django.db.backends.sqlite3', 
                            'NAME': 'dev',                      
                            'USER': '',                      
                            'PASSWORD': '',                  
                            'HOST': '',                      
                            'PORT': '',                     
                }
    } 

MONGO_DATABASES = {
    # db_name, db_alias
    'neerbee': 'default', 
}

MONGO_DATABASE_NAME = os.environ['MONGO_DATABASE_NAME']

import mongoengine
#use the following when deploying on heroku:
if os.environ.get('MONGOHQ_URL'):
    mongoengine.connect(MONGO_DATABASE_NAME, host=os.environ['MONGOHQ_URL'])
else:
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = int(os.environ['MONGO_PORT'])
    mongoengine.connect(MONGO_DATABASE_NAME, host=MONGO_HOST, port=MONGO_PORT)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Athens'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
    ('el', 'Greek'),
)

LOCALE_PATHS = (
    './locale',
)

SITE_ID = 1
SITE = os.environ['SITE']
SITE_NAME = 'neerbee'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = path('./media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path('./static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    "./media",
    "./static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5%5x$##n4en&amp;=j834%u=v8c_ozq0bvd5%ev60cpla5p#vck(_#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'neerbee.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'neerbee.wsgi.application'

TEMPLATE_DIRS = (
        './templates',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin',
    'accounts',
    'spots',
    'users',
    'registration',
    'tastypie',
    'tastypie_mongoengine',
    'mongotesting',
)

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window

AUTHENTICATION_BACKENDS = (
    'users.auth_backend.BeeAuthBackend',
)

SESSION_ENGINE = 'mongoengine.django.sessions'

DEFAULT_FORM_EMAIL = 'hello@neerbee.com'

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

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

LOGIN_REDIRECT_URL = '/'