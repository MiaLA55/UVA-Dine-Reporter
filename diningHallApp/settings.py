from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


AWS_ACCESS_KEY_ID = "AKIAU6GD2ERXH4XMKEH5"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "dininghallapp"
AWS_URL = "https://dininghallapp.s3.amazonaws.com/"
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = "us-east-2"
AWS_S3_SIGNATURE_VERSION = "s3v4"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")


SITE_ID = 2

# Application definition

INSTALLED_APPS = [
    "login",
    "file_upload",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "bootstrap5",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "diningHallApp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "../templates"), ],
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


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"


USE_I18N = True

USE_L10N = True

USE_TZ = True

# DATETIME_FORMAT = "Y-m-d H:i:sO"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = AWS_URL + "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# STATIC_URL = "static/"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_URL = AWS_URL + "/media/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "1061490713677-lco3blmvsce1jp0k1i91rnvff2t4fm99.apps.googleusercontent.com"
)

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": "1061490713677-lco3blmvsce1jp0k1i91rnvff2t4fm99.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
    }
}
SITE_ID = 2

LOGIN_REDIRECT_URL = "/auth_home/"
LOGOUT_REDIRECT_URL = "/logout/"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "uva-dining-hall-reporter-32168ccd03da.herokuapp.com",
]

WSGI_APPLICATION = "diningHallApp.wsgi.application"

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ
# SECURITY WARNING: don't run with debug turned on in production!
# if not IS_HEROKU_APP:
DEBUG = True

if IS_HEROKU_APP:
    # In production on Heroku the database configuration is derived from the `DATABASE_URL`
    # environment variable by the dj-database-url package. `DATABASE_URL` will be set
    # automatically by Heroku when a database addon is attached to your Heroku app. See:
    # https://devcenter.heroku.com/articles/provisioning-heroku-postgres
    # https://github.com/jazzband/dj-database-url
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }
else:
    # When running locally in development or in CI, a sqlite database file will be used instead
    # to simplify initial setup. Longer term it's recommended to use Postgres locally too.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            # "ENGINE": "django.db.backends.postgresql_psycopg2",
            # "NAME": "db",
            # "USER": "a-29-member",
            # "PASSWORD": "!S24ASDA29Group!",
            # "HOST": "localhost",
            # "PORT": "5432",
        }
    }

# STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

# MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# SHERRIFF
# Activate Django-Heroku.
# Use this code to avoid the psycopg2 / django-heroku error!
# Do NOT import django-heroku above!
try:
    if "HEROKU" in os.environ:
        import django_heroku

        django_heroku.settings(locals())
except ImportError:
    found = False
