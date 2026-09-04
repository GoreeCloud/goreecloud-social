from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parents[2]
ENVIRONMENT = os.getenv("SOCIAL_ENV", "development").strip().lower()

SECRET_KEY = os.getenv("SOCIAL_SECRET_KEY", "")
if not SECRET_KEY:
    if ENVIRONMENT == "production":
        raise ImproperlyConfigured("SOCIAL_SECRET_KEY is required in production")
    SECRET_KEY = "development-only-not-for-production"

DEBUG = ENVIRONMENT != "production"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("SOCIAL_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1],testserver").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "social",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "goreecloud_social.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]

WSGI_APPLICATION = "goreecloud_social.wsgi.application"
ASGI_APPLICATION = "goreecloud_social.asgi.application"

sqlite_path = Path(os.getenv("SOCIAL_SQLITE_PATH", str(BASE_DIR / "var" / "social.sqlite3")))
sqlite_path.parent.mkdir(parents=True, exist_ok=True)
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": sqlite_path}}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
