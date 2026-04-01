from pathlib import Path
import os
import sys
import dj_database_url   # ✅ NEW

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

    # 🔥 CHANNELS (optional - Vercel doesn't support websocket)
    # 'channels',

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

                'apps.courses.context_processors.chatbot_courses',
            ],
        },
    },
]


# =========================================
# 🔥 DATABASE (NEON POSTGRESQL FIX)
# =========================================

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}


# ✅ PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = []


# =========================================
# ✅ STATIC FILES
# =========================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# =========================================
# ✅ MEDIA FILES
# =========================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ✅ DEFAULT FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================
# 🔥 CHANNELS (DISABLED FOR VERCEL)
# =========================================

# ASGI_APPLICATION = 'E_learning.asgi.application'

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",
#     },
# }


# =========================================
# 🔥 VERCEL FIX
# =========================================

if 'vercel' in sys.argv:
    DEBUG = True