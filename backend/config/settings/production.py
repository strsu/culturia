from config.settings.base import *
from config.cron_jobs import *

DEBUG = False

CRONTAB_DJANGO_SETTINGS_MODULE = "config.settings.production"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

WSGI_APPLICATION = "config.wsgi.application"

CORS_ORIGIN_WHITELIST = [
    "http://anhae.site",
    "https://anhae.site",
    "http://localhost",
    "https://localhost",
    "https://172.104.96.127",
]
CSRF_TRUSTED_ORIGINS = [
    "http://anhae.site",
    "https://anhae.site",
    "http://localhost",
    "https://localhost",
    "https://172.104.96.127",
]
