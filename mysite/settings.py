import os

# fix warnings for new Django version
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""
ALLOWED_HOSTS = ["127.0.0.1"]

if os.getenv("SECRET_KEY"):
    SECRET_KEY = os.getenv("SECRET_KEY")
else:
    SECRET_KEY = "<EXAMPLE-SECRET-KEY-NOT-VERY-SECURE>"

DOMAIN = ""

if os.getenv("DOMAIN"):
    DOMAIN = os.getenv("DOMAIN")
    ALLOWED_HOSTS.append(DOMAIN)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#Session Management
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_WARN_AFTER = 300 #warn user after 4m that session will expire
SESSION_SECURITY_EXPIRE_AFTER = 600 #logout after 5m
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 24*60*60
SESSION_COOKIE_NAME = 'TRSYNC-SESS'
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True #https only
CSRF_COOKIE_SECURE = True #https only
CSRF_FAILURE_VIEW = 'polls.views.error_csrf'

# HTTPS settings
SECURE_HSTS_SECONDS = "31536000"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
REFERRER_POLICY = 'same-origin'
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", 'fonts.googleapis.com', 'cdn.datatables.net')
CSP_SCRIPT_SRC = ("'self'","'unsafe-inline'", "'unsafe-eval'", 'code.jquery.com', 'cdn.datatables.net', 'cdnjs.cloudflare.com')
CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com',)
CSP_IMG_SRC = ("'self'", 'data:', 'avatarfiles.alphacoders.com', 'cdn.datatables.net','aktiengram.de',)
CSP_OBJECT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'session_security',
    'django_http_referrer_policy',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django_http_referrer_policy.middleware.ReferrerPolicyMiddleware',
    #'csp.middleware.CSPMiddleware',
]

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
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
    },
}

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'
LOGIN_URL = '/index'
LOGIN_REDIRECT_URL = '/index'
LOGOUT_REDIRECT_URL = '/index'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database', 'db.sqlite3'),
    }
}

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/opt/TRSync/static/'
MEDIA_ROOT = '/opt/TRSync/mysite/media/'
