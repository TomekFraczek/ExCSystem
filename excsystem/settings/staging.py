import django_heroku
import sentry_sdk

from excsystem.settings.base import *

sentry_sdk.init("https://7f55db81d88d4875aeb5e21bce8655aa@sentry.io/1314232")

STATIC_URL = "static/"
MEDIA_URL = "media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DJANGO_DEBUG", False))
ALLOWED_HOSTS = ["excsystem.herokuapp.com"]

# Email host settings
EMAIL_HOST = "localhost"
EMAIL_PORT = 1024
MEMBERSHIP_EMAIL_HOST_USER = "membership@ExCDev.org"
MEMBERSHIP_EMAIL_HOST_PASSWORD = ""
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Base address of where the page is available
WEB_BASE = "https://www.excsystem.herokuapp.com"
SITE_DOMAIN = "www.excsystem.herokuapp.com"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "%(levelname)s %(asctime)s [%(name)s] %(message)s",
        }
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/debug.log",
            "formatter": "django.server",
        },
        "request_handler": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/requests.log",
            "formatter": "django.server",
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "console_debug_false": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "DEBUG", "propagate": True},
        "django": {"handlers": ["console", "console_debug_false"], "level": "INFO"},
        "django.request": {
            "handlers": ["request_handler"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

django_heroku.settings(locals())
