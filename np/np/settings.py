from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fbgln&_arnkv2dxez-b&=2v7y&rz22d@p+$9d1r0l6yk+6$u7c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['neuropink.rs', 'www.neuropink.rs']
# ALLOWED_HOSTS = ['*']

ADMINS = [('Marko', 'k0m4r4c00@gmail.com'),
          ('Saša', 'sasamilosevic.1992@gmail.com')]
# Application definition
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zeptomail.eu'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'emailapikey'
EMAIL_HOST_PASSWORD = 'yA6KbHtYvVqkxzhQSRNs1JfepdxjpaA+iSq34CvrKcZyftaziKE91Rtqcdroc2GI0IHX5KlTbd1Cdtq6uN5efsY8MdRZKZTGTuv4P2uV48xh8ciEYNYhhpuqAbkRGqRLdxgtCyg1Q/AlWA== '
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Neuropink - '
SERVER_EMAIL = 'neuropink.rs <noreply@neuropink.rs>'
DEFAULT_FROM_EMAIL = 'neuropink.rs <noreply@neuropink.rs>'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'neuropink'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'neuropink.middleware.Log400Middleware',
]

ROOT_URLCONF = 'np.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'conv_int': 'neuropink.templatetags.conv_int',
            }
        },
    },
]

WSGI_APPLICATION = 'np.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neuropink',
        'USER': 'postgres',
        'PASSWORD': 'K0marchina!',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Belgrade'

USE_I18N = True

USE_TZ = True

CSRF_TRUSTED_ORIGINS = [
    'https://neuropink.rs',
    'https://www.neuropink.rs',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # your app-level static
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/home/marko/projects/neuropink/logs/neuropink.log',
#             'formatter': 'verbose',
#         },
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file', 'console'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#         'django.request': {
#             'handlers': ['file', 'console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'django.security': {
#             'handlers': ['file', 'console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }
