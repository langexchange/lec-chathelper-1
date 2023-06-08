from pathlib import Path
import environ
import os 

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR,'env/.dev.env'))


######### LANGEXCHANGE CUSTOM CONFIGURATION #########
#####################################################

## ENVIRONMENT VARS
LANGGENERAL_DB = env("LANGGENERAL_DB")
LANGGENERAL_DB_HOST = env('LANGGENERAL_DB_HOST')
LANGGENERAL_PASS = env("LANGGENERAL_PASS")
LANGGENERAL_USER = env("LANGGENERAL_USER")
LANGGENERAL_PORT = env("LANGGENERAL_PORT")

LANGCHAT_DB = env("LANGCHAT_DB")
LANGCHAT_DB_HOST = env('LANGCHAT_DB_HOST')
LANGCHAT_PASS = env("LANGCHAT_PASS")
LANGCHAT_USER = env("LANGCHAT_USER")
LANGGENERAL_PORT = env("LANGGENERAL_PORT")
LANGCHAT_PORT = env("LANGCHAT_PORT")
WEB_SERVER_HOST = env("WEB_SERVER_HOST")

CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_BROKER_URL = env("CELERY_BROKER_URL")

## DATABASEs
DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        'HOST': LANGCHAT_DB_HOST,
        'NAME': LANGCHAT_DB, 
        'USER': LANGCHAT_USER,
        'PASSWORD': LANGCHAT_PASS,
        'PORT': LANGCHAT_PORT,
    },

    'langgeneral': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        'HOST': LANGGENERAL_DB_HOST,
        'NAME': LANGGENERAL_DB, 
        'USER': LANGGENERAL_USER,
        'PASSWORD': LANGGENERAL_PASS,
        'PORT': LANGGENERAL_PORT,
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': "{}/db.sqlite3".format(BASE_DIR),
    # },
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# REST
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# CELERY CONFIGURATIONS
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"
CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
CELERY_BROKER_URL = CELERY_BROKER_URL
CELERY_HIJACK_ROOT_LOGGER = False
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
    'retry_policy': {
       'timeout': 5.0
    }
}


# HOST ACCESS CONTROL
ALLOWED_HOSTS = ["localhost",  WEB_SERVER_HOST]


# APPS DEFINITION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat.apps.ChatConfig',
    'rest_framework',
    'django_prometheus',
]

MIGRATION_MODULES = {'chat': 'chat.notmigrations'}

DATABASE_ROUTERS = ['chat.dbrouter.ChatRouter']

# TESTING
TEST_RUNNER = 'lec_chathelper.test_runner.ExampleTestRunner'
######### END LANGEXCHANGE CUSTOM CONFIGURATION #########
#####################################################




# Build paths inside the project like this: BASE_DIR / 'subdir'.



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
SECRET_KEY_FALLBACKS = [
    env('OLD_SECRET_KEY'),
]

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False


MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'lec_chathelper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'lec_chathelper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


