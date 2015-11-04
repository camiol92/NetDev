"""
Django settings for DjangoProject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_DIR = os.path.abspath(PROJECT_PATH)

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)


#cooekis settings
# SESSION_COOKIE_AGE = 604800
#
# #django-registration-redux settings
# REGISTRATION_OPEN = True                # If True, users can register
# ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
# REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
# LOGIN_REDIRECT_URL = '/netdev/'  # The page you want users to arrive at after they successful log in
# LOGIN_URL = '/netdev/registrar/'  # The page users are directed to if they are not logged in,
#                                                                 # and are trying to access pages requiring authentication

DATABASE_PATH = os.path.join(PROJECT_PATH, 'netdev.db')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&u#=aek)j+$_-nbj91m+ipr5)so)e)2r+56dl*ix@idy8h5gw3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
   # 'django.contrib.sites', talvez seja necessario para user auth
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'netdev',
    'bootstrap3',
    'bootstrap_toolkit',
    'i18n'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'DjangoProject.urls'

WSGI_APPLICATION = 'DjangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH
    }
}

DATABASE_PATH = os.path.join(PROJECT_PATH, 'netdev.db')

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/accounts/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(PROJECT_PATH,'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media') # Absolute path to the media directory