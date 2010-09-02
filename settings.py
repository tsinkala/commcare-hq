#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import os, time

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS


# default to the system's timezone settings. this can still be
# overridden in rapidsms.ini [django], by providing one of:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = time.tzname[0]


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Django i18n searches for translation files (django.po) within this dir
LOCALE_PATHS=['contrib/locale']

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2rgmwtyq$thj49+-6u7x9t39r7jflu&1ljj3x2c0n0fl$)04_0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corehq.apps.domain.middleware.DomainMiddleware',
]

ROOT_URLCONF = "urls"

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "corehq.util.context_processors.base_template" # sticks the base template inside all responses
]

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]

BASE_TEMPLATE = "layout.html"
LOGIN_TEMPLATE="login_and_password/login.html"
LOGGEDOUT_TEMPLATE="loggedout.html"

# ====================
# INJECT RAPIDSMS APPS
# ====================
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
)

HQ_APPS = (
    'corehq.lib.django_granular_permissions',
    'corehq.lib.django_rest_interface',
    'corehq.lib.django_tables',
    'corehq.lib.django_user_registration',
    'corehq.apps.domain',
    'corehq.apps.docs',
    # pull in anton's fixes to make logtracker work on hq's
    #'corehq.apps.logtracker',
    'corehq.apps.releasemanager',
    'corehq.apps.requestlogger',
    'corehq.apps.receiver',
    'corehq.apps.hqwebapp',
    'corehq.apps.program',
    'corehq.apps.phone',
    # lame: xforms needs to be run last
    # because it resets xmlrouter, which breaks functionality in
    # other code which is dependent on xmlrouter's global initialization
    'corehq.apps.xforms',
    'graphing',
    'ota_restore'
)

INSTALLED_APPS = DEFAULT_APPS + HQ_APPS


# after login, django redirects to this URL
# rather than the default 'accounts/profile'
LOGIN_REDIRECT_URL='/'


####### Domain settings  #######

DOMAIN_MAX_REGISTRATION_REQUESTS_PER_DAY=99
DOMAIN_SELECT_URL="/domain/select/"
LOGIN_URL="/accounts/login/"
# For the registration app
# One week to confirm a registered user account
ACCOUNT_ACTIVATION_DAYS=7 
# If a user tries to access domain admin pages but isn't a domain 
# administrator, here's where he/she is redirected
DOMAIN_NOT_ADMIN_REDIRECT_PAGE_NAME="homepage"

####### Release Manager App settings  #######
RELEASE_FILE_PATH=os.path.join("data","builds")

####### Photo App settings  #######
PHOTO_IMAGE_PATH=os.path.join("data","photos")


####### Shared/Global/UI Settings ######

# restyle some templates
BASE_TEMPLATE="hq-layout.html"
LOGIN_TEMPLATE="login_and_password/login.html"
LOGGEDOUT_TEMPLATE="loggedout.html"



# email settings: these ones are the custom hq ones
EMAIL_LOGIN="notifications@dimagi.com"
EMAIL_PASSWORD="alpha321"
EMAIL_SMTP_HOST="smtp.gmail.com"
EMAIL_SMTP_PORT=587

# these are the official django settings
# which really we should be using over the
# above
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "notifications@dimagi.com"
EMAIL_HOST_PASSWORD = "alpha321"
EMAIL_USE_TLS = True


TABS = [
    ('corehq.apps.hqwebapp.views.dashboard', 'Dashboard'),
    ('corehq.apps.releasemanager.views.projects', 'Release Manager'),
    ('corehq.apps.receiver.views.show_submits', 'Submissions'),
    ('corehq.apps.xforms.views.dashboard', 'XForms'),
    ('graphing.views.domain_charts', 'Charts'),
]

# import local settings if we find them
try:
    from localsettings import *
except ImportError:
    pass

# create data directories required by commcarehq
import os
root = os.path.dirname(__file__)
if not os.path.isdir(os.path.join(root,'data')):
    os.mkdir(os.path.join(root,'data'))
if not os.path.isdir(os.path.join(root,'data','submissions')):
    os.mkdir(os.path.join(root,'data','submissions'))
if not os.path.isdir(os.path.join(root,'data','attachments')):
    os.mkdir(os.path.join(root,'data','attachments'))
if not os.path.isdir(os.path.join(root,'data','schemas')):
    os.mkdir(os.path.join(root,'data','schemas'))


# FEEL FREE TO PUT THIS IN YOUR LOCALSETTINGS.PY
DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'commcarehq'       # Or path to database file if using sqlite3.
DATABASE_USER = 'root'     # Not used with sqlite3.
DATABASE_PASSWORD = 'password'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DJANGO_LOG_FILE = "/var/log/commcarehq/commcarehq.django.log"
LOG_SIZE = 1000000
LOG_LEVEL   = "ERROR"
LOG_FILE    = "/var/log/commcarehq/commcarehq.log"
LOG_FORMAT  = "[%(name)s]: %(message)s"
LOG_BACKUPS = 256 # number of logs to keep


####### Receiver Settings #######
ROOT_DATA_PATH = "data"
RECEIVER_SUBMISSION_PATH=ROOT_DATA_PATH + "/submissions"
RECEIVER_ATTACHMENT_PATH=ROOT_DATA_PATH + "/attachments"
RECEIVER_EXPORT_PATH=ROOT_DATA_PATH

####### XFormManager Settings #######
XFORMS_SCHEMA_PATH=ROOT_DATA_PATH + "/schemas"
XFORMS_EXPORT_PATH=ROOT_DATA_PATH
XFORMS_FORM_TRANSLATE_JAR="corehq/lib/form_translate.jar"

