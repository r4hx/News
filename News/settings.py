import os
from pathlib import Path

from django.conf.locale.en import formats as en_formats

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

AUTH_USER_MODEL = "Account.CustomUser"
DEBUG = os.getenv("DEBUG", "False")

APP_ENV = os.getenv("APP_ENV")
if not APP_ENV:
    raise Exception("APP_ENV is not set")

APP_SITE_ADDRESS = os.getenv("APP_SITE_ADDRESS")
if not APP_SITE_ADDRESS:
    raise Exception("APP_SITE_ADDRESS is not set")

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=APP_ENV,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        ignore_errors=[],
    )

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise Exception("DJANGO_SECRET_KEY is not set")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
if not ALLOWED_HOSTS:
    raise Exception("ALLOWED_HOSTS is not set")

CSRF_TRUSTED_ORIGINS = [os.getenv("CSRF_TRUSTED_ORIGINS")]
if not CSRF_TRUSTED_ORIGINS:
    raise Exception("CSRF_TRUSTED_ORIGINS is not set")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Account",
    "Rss",
    "Web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "News.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Feed.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "CONN_MAX_AGE": 60 * 10,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

en_formats.DATETIME_FORMAT = "d.m.Y H:i:s"
en_formats.DATE_FORMAT = "d.m.Y"
en_formats.TIME_FORMAT = "H:i:s"
en_formats.SHORT_DATE_FORMAT = "d.m.Y"
en_formats.SHORT_DATETIME_FORMAT = "d.m.Y H:i:s"

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True


STATIC_ROOT = "static/"
STATIC_URL = "static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")

CELERY_BROKER_URL = f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_SEND_EVENTS = False
CELERY_WORKER_ENABLE_REMOTE_CONTROL = False
