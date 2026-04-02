from pathlib import Path
import os
import sys
import dj_database_url

# ☁️ CLOUDINARY
import cloudinary
import cloudinary.uploader
import cloudinary.api

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

    # YOUR APPS
    'apps.accounts',
    'apps.courses',
    'apps.payments',
    'apps.analytics',

    # ☁️ CLOUDINARY (IMPORTANT)
    'cloudinary',
    'cloudinary_storage',
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
# 🔥 DATABASE (NEON POSTGRESQL)
# =========================================

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}


# =========================================
# 🔑 PASSWORD VALIDATION
# =========================================

AUTH_PASSWORD_VALIDATORS = []


# =========================================
# 🌍 LANGUAGE
# =========================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# =========================================
# 📁 STATIC FILES
# =========================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# =========================================
# ❌ MEDIA FILES (DISABLED FOR VERCEL)
# =========================================

MEDIA_URL = '/media/'


# =========================================
# ☁️ CLOUDINARY CONFIG (🔥 MAIN FIX)
# =========================================

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('API_KEY'),
    'API_SECRET': os.environ.get('API_SECRET'),
}
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# =========================================
# 🔢 DEFAULT FIELD
# =========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================
# 🔥 VERCEL FIX
# =========================================

if 'vercel' in sys.argv:
    DEBUG = True