from config.settings.base import *
from config.cron_jobs import *

DEBUG = True

CRONTAB_DJANGO_SETTINGS_MODULE = "config.settings.development"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": ENV["POSTGRES_DB"],
        "USER": ENV["POSTGRES_USER"],
        "PASSWORD": ENV["POSTGRES_PASSWORD"],
        "HOST": ENV["POSTGRES_HOST"],
        "PORT": ENV["POSTGRES_PORT"],
    }
}

WSGI_APPLICATION = "config.wsgi.application"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "https://localhost",
    "https://192.168.1.243",
]
