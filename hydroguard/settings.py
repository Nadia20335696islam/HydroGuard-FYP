"""
Django settings for HydroGuard project.

This file contains all configuration settings for the Django application,
including installed apps, middleware, database setup, and security settings.
"""

from pathlib import Path

# --------------------------------------------------
# BASE DIRECTORY CONFIGURATION
# --------------------------------------------------
# BASE_DIR points to the root directory of the project.
# It is used to build paths for database, static files, etc.
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SECURITY SETTINGS
# --------------------------------------------------

# Secret key used for cryptographic signing.
# IMPORTANT: Keep this key confidential in production.
SECRET_KEY = 'django-insecure-k!-%*2o(uc)!sifna&#64b+0a6vi@o8w+e24x6x@h&3l3h-_b-'

# Debug mode (True for development, False for production)
DEBUG = True

# List of allowed host/domain names
ALLOWED_HOSTS = []


# --------------------------------------------------
# APPLICATION DEFINITION
# --------------------------------------------------

INSTALLED_APPS = [
    # Django built-in apps (required for core functionality)
    'django.contrib.admin',          # Admin panel
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content type system
    'django.contrib.sessions',       # Session management
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static files (CSS, JS)

    # Custom project apps
    'accounts',  # Handles user authentication and profiles
    'usage',     # Will handle water usage tracking
    'core',      # General views (home, dashboard, etc.)
    'goals',     # user set goals to achieve
    'gamification.apps.GamificationConfig',  # Handles points, badges, streaks, and level progression
    'community',  # Handles community posts, comments, and likes
]


# --------------------------------------------------
# MIDDLEWARE CONFIGURATION
# --------------------------------------------------
# Middleware processes requests/responses globally.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',              # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',       # Session support
    'django.middleware.common.CommonMiddleware',                  # Common HTTP operations
    'django.middleware.csrf.CsrfViewMiddleware',                  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',    # Enables authentication
    'django.contrib.messages.middleware.MessageMiddleware',       # Messaging support
    'django.middleware.clickjacking.XFrameOptionsMiddleware',     # Clickjacking protection
]


# --------------------------------------------------
# URL CONFIGURATION
# --------------------------------------------------
# Root URL configuration file
ROOT_URLCONF = 'hydroguard.urls'


# --------------------------------------------------
# TEMPLATES CONFIGURATION
# --------------------------------------------------
# Defines how HTML templates are loaded and rendered.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add global template directory if needed
        'APP_DIRS': True,  # Enables templates inside app folders
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Access request in templates
                'django.contrib.auth.context_processors.auth', # Auth context (user)
                'django.contrib.messages.context_processors.messages',  # Messages
            ],
        },
    },
]


# --------------------------------------------------
# WSGI APPLICATION
# --------------------------------------------------
# Entry point for WSGI-compatible web servers
WSGI_APPLICATION = 'hydroguard.wsgi.application'


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------
# Using SQLite for development (simple and built-in)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
# Built-in Django validators for strong password security

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


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/London'

USE_I18N = True  # Enable translation system
USE_TZ = True    # Enable timezone-aware datetimes


# --------------------------------------------------
# STATIC FILES (CSS, JavaScript, Images)
# --------------------------------------------------

STATIC_URL = 'static/'


# --------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# --------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'