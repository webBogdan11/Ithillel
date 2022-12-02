import environ
from pathlib import Path
from celery.schedules import crontab

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY=env('SECRET_KEY', default='SECRET_KEY')  # noqa

DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my apps
    'orders',
    'feedback',
    'users',
    'products',
    'currencies',
    'favorite',
    # extensions
    'django_celery_results',
    'django_celery_beat',
    'silk'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = ['static_dev']

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login/'
LOGOUT_URL = 'logout/'

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = 'django_celery_results.backends.database.DatabaseBackend'

CELERY_BEAT_SCHEDULE = {
    'Get currency': {
        'task': 'currencies.tasks.get_currencies',
        'schedule': crontab(minute='3'),
    }
}

CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        # 'LOCATION': env('MEMCACHE_LOCATION', default='MEMCACHE_LOCATION'),
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'django_cache',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.PhoneModelBackend'
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT', default='EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)

ADMINS = [('Bohdan', env('ADMIN_EMAIL', default='ADMIN_EMAIL'))]
MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = 'Super shop - '
SERVER_EMAIL = EMAIL_HOST_USER
