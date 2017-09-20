
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR, ]
PROJECT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_URL = '/login/'  # @login_required decoratorü için. eğer user login olmamışsa buraya yönlendirir
LOGIN_REDIRECT_URL = '/'  # login olduktan sonra redirect edilecek url (index)

# Güvenlik nedenlerinden dolayı bu keyi kaybetmeyin/gizli tutun. aksi taktirde db üzerindeki hashli tüm veriler
# tehlikeye girer/okunamaz
SECRET_KEY = 'dw*vszsn+q!n&_8t(tjg5$5(s(@i+)2kvfat!q=r+^4-pr&-1k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_HOST = 'smtp.yandex.com.tr'
EMAIL_HOST_USER = 'mailadmin@buraktopal.xyz'
EMAIL_HOST_PASSWORD = 'selam123'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_BACKEND = "fisher_mailer.backend.DbBackend"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'fisher_app',
    'geoposition',
    'corsheaders',
    'fisher_mailer',
    'django_user_agents'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = 'fisher.urls'

USER_AGENTS_CACHE = None

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'media', 'files', 'templates')],
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

WSGI_APPLICATION = 'fisher.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fisherdb',
        'USER': 'fisher',
        'PASSWORD': 'selam123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    
    'PAGE_SIZE': 100  # pagination
}

GEOIP_PATH = os.path.join(BASE_DIR, 'Geolocation')

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

DOMAIN = "localhost"

LANGUAGE_CODE = 'tr-tr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyCIFErzxS2TJQXL4FYxrREnPjyyrtNjszk'  # geçici key

GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 15,
    'zoom': 8,
    'center': {'lat': 38.425592, 'lng': 27.138988},
    'scrollwheel': True
}
