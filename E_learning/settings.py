from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'secret'

DEBUG = True

ALLOWED_HOSTS = ['*']


# ✅ CUSTOM USER MODEL
AUTH_USER_MODEL = 'accounts.User'


# ✅ INSTALLED APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🔥 CHANNELS
    'channels',

    # YOUR APPS
    'apps.accounts',
    'apps.courses',
    'apps.payments',
    'apps.analytics',
]


# ✅ AUTH BACKEND
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# ✅ MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


# ✅ ROOT URL
ROOT_URLCONF = 'E_learning.urls'


# ✅ TEMPLATES
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

                # ✅ YOUR CONTEXT PROCESSOR
                'apps.courses.context_processors.chatbot_courses',
            ],
        },
    },
]


# ✅ DATABASE (FIXED FOR VERCEL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',   # 🔥 IMPORTANT FIX
    }
}


# ✅ PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = []


# ✅ STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 🔥 IMPORTANT


# ✅ MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ✅ DEFAULT FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================
# 🔥 CHANNELS (WEBSOCKET SUPPORT)
# =========================================

ASGI_APPLICATION = 'E_learning.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# =========================================
# 🔥 VERCEL FIX (IMPORTANT)
# =========================================

if 'vercel' in sys.argv:
    DEBUG = True