import os
from website.settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['165.227.33.196', 'hellowebbooks.com', '.hellowebbooks.com',]

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hellowebbooks',
        'USER': os.environ['POSTGRES_US'],
        'PASSWORD': os.environ['POSTGRES_PW'],
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'hwb@mg.hellowebbooks.com'
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_API']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STRIPE_PUBLISHABLE = 'pk_live_iYx3AwCFDTtVOu7qP1B9UFsa'
