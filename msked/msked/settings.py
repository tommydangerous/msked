# Django settings for msked project.
import os, socket

# Check environment
if os.environ.get('MYSITE_PRODUCTION', False):
    # production
    DEBUG = TEMPLATE_DEBUG = False
    DEV = False
    COMPRESS_ENABLED = True
else:
    # development
    DEBUG = TEMPLATE_DEBUG = True
    DEV = True
    COMPRESS_ENABLED = False

project_name = 'msked'

ADMINS = (
    ('Tommy Dang', 'tommydangerouss@gmail.com')
)

AUTHENTICATION_BACKENDS = (
    'msked.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Amazon S3
AWS_ACCESS_KEY_ID = 'AKIAIXM2DMH4M2PAT5TA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = project_name
if DEV:
    BUCKET_NAME = project_name + '_development'
else:
    BUCKET_NAME = project_name

AWS_HEADERS = {
    'Expires': 'Sun, 19 Jul 2020 18:06:32 GMT'
}

AWS_QUERYSTRING_AUTH = False

if DEV:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     '%s' % project_name,
            'USER':     'postgres',
            'PASSWORD': 'postgres',
            'HOST':     '',
            'PORT':     '5432',
        }
    }
else:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
    }

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LOGIN_URL = '/login/'

MANAGERS = ADMINS

# Absolute filesystem path to the directory that will hold user-uploaded files.
if DEV:
    MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 
        'media')).replace('\\', '/').replace('\%s' % project_name, '/%s' % project_name)
else:
    MEDIA_ROOT = os.path.dirname(__file__).replace('\\','/') + '/../media'

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Message
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'msked.urls'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j9@5%gy&amp;(+0&amp;q!b&amp;0mjbfx$1%a15@5t&amp;g&amp;7hgmxj9ksm704z)='

# Session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Absolute path to the directory static files should be collected to.
if DEV:
    STATIC_ROOT = ''
else:
    STATIC_ROOT = os.path.dirname(
        __file__).replace('\\','/') + '/../static'

# URL prefix for static files.
if DEV:
    STATIC_URL = '/static/'
else:
    STATIC_URL = 'http://s3.amazonaws.com/%s/' % project_name

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 
        'static')).replace('\\', '/').replace(
            '\%s' % project_name, '/%s' % project_name),
)

# List of finder classes that know how to find static files in
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # other finders
    'compressor.finders.CompressorFinder',
)

# static file server
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 
        'templates')).replace('\\', '/').replace(
            '\%s' % project_name, '/%s' % project_name),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'msked.wsgi.application'

# Django Compressor Amazon S3
COMPRESS_URL = 'http://s3.amazonaws.com/%s/' % project_name
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

INSTALLED_APPS += (
    'compressor',
    'south',
    'storages',
)

INSTALLED_APPS += (
    'assignments',
    'employees',
    'excludes',
    'job_schedules',
    'jobs',
    'location_schedules',
    'locations',
    'notes',
    'placements',
    'requires',
    'schedules',
    'seats',
    'stations',
    'tasks',
    'teams',
    'undos',
    'users',
    'works',
)

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
