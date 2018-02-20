USE_TZ = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "example.sqlite",
    }
}

ROOT_URLCONF = "django_pwn.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_pwn",
]

SECRET_KEY = "42"

TEMPLATES = [
    {
        'OPTIONS': {
            'debug': True,
        }
    }
]

SITE_ID = 1