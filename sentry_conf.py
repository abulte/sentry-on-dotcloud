
import os.path
import json

with open(os.path.expanduser('~/environment.json'), 'r') as env_file:
    dotcloud_env = json.load(env_file)

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        # You can swap out the engine for MySQL easily by changing this value
        # to ``django.db.backends.mysql`` or to PostgreSQL with
        # ``django.db.backends.postgresql_psycopg2``
        'ENGINE': 'django.db.backends.mysql',
        # Update DATABASE_URL in mkadmin.py if you choose another database name
        'NAME': 'sentry',
        'USER': dotcloud_env['DOTCLOUD_DB_MYSQL_LOGIN'],
        'PASSWORD': dotcloud_env['DOTCLOUD_DB_MYSQL_PASSWORD'],
        'HOST': dotcloud_env['DOTCLOUD_DB_MYSQL_HOST'],
        'PORT': int(dotcloud_env['DOTCLOUD_DB_MYSQL_PORT']),
    }
}

# Disable Django admins settings, we are going to use Sentry's settings
ADMINS = ()
SENTRY_ADMINS = (dotcloud_env['SENTRY_ADMIN'])

SENTRY_KEY = dotcloud_env['SENTRY_KEY']

# Set this to false to require authentication
SENTRY_PUBLIC = False

# You should configure the absolute URI to Sentry. It will attempt to guess it if you don't
# but proxies may interfere with this.
SENTRY_URL_PREFIX = dotcloud_env.get('SENTRY_URL_PREFIX', '') # No trailing slash!

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = dotcloud_env['PORT_SENTRYWEB']
SENTRY_WEB_OPTIONS = {
    'workers': 2,  # the number of gunicorn workers
    'worker_class': 'gevent',
}

# UDP Server

SENTRY_UDP_HOST = '0.0.0.0'
SENTRY_UDP_PORT = dotcloud_env['PORT_SENTRYUDP']

# Mail server configuration

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# Configure the Queue and the Buffers to process incoming events asynchronously:

SENTRY_USE_QUEUE = True

BROKER_URL = '{url}/{database}'.format(url=dotcloud_env['DOTCLOUD_BUFFERS_REDIS_URL'], database=0)
CELERY_IGNORE_RESULT = True
CELERY_SEND_EVENTS = False
CELERY_SEND_TAKS_ERROR_EMAILS = True

SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
SENTRY_BUFFER_OPTIONS = {
    'hosts': {
        0: {
            'host': dotcloud_env['DOTCLOUD_BUFFERS_REDIS_HOST'],
            'port': int(dotcloud_env['DOTCLOUD_BUFFERS_REDIS_PORT']),
            'password': dotcloud_env['DOTCLOUD_BUFFERS_REDIS_PASSWORD'],
            'db': 1
        }
    }
}

# Enable the middleware to force SSL on the web interface. Usually you would do
# a redirecet on the reverse proxy that terminates SSL but you can't configure
# these proxies on dotCloud and I don't want to embed an Nginx process inside
# this service just to do a redirect.
#
# XXX: I guess this will break POSTs to the Sentry API using HTTP.
EXTRA_MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
)
