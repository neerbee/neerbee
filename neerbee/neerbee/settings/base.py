# settings/base.py
import os

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an eception.
from django.core.exceptions import ImproperlyConfigured

from unipath import Path

def get_env_variable(var_name):
    """ Get the environment variable or return exception. """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

# The full path to the django website directory
PROJECT_ROOT = Path(__file__).ancestor(3)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tastypie',
    'tastypie_mongoengine',
    'accounts',
    'admin',
    'registration',
    'spots',
    'users',
)

LOCALE_PATHS = (
   PROJECT_ROOT.child('locale'), 
)

MONGO_DATABASES = {
    # db_name, db_alias
    'neerbee': 'default',
}

MONGO_DATABASE_NAME = 'neerbee'

SECRET_KEY = get_env_variable('SECRET_KEY')

TEMPLATE_CONTEXT_PROCESSORS = (
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
)

