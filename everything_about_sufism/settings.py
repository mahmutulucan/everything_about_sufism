"""
Django settings for everything_about_sufism project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/.
"""

import dj_database_url
import os
from pathlib import Path

from django.contrib.messages import constants as messages

from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Project Configuration
# -----------------------------------------------------------------------------

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the .env file for secure configuration.
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path)

# -----------------------------------------------------------------------------
# Standard Django Settings
# -----------------------------------------------------------------------------

# Ensure the secret key is securely loaded from environment variables.
# This key is critical for cryptographic signing; keep it secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if SECRET_KEY is None:
    raise ValueError(
        'The SECRET_KEY environment variable is not set.'
    )

# Set debug mode based on environment variable. Avoid enabling in production.
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# List of allowed host/domain names for this Django site.
# Important for production to prevent HTTP Host header attacks.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')
    
# Application definition
INSTALLED_APPS = [
    # Local apps
    'pages',
    'content',
    'user',

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django_ckeditor_5',
    'cloudinary',
    'cloudinary_storage',

    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware configuration for handling requests and responses
MIDDLEWARE = [
    # Django default middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware for additional functionalities
    'user.middleware.UnreadMessagesMiddleware',
    'user.middleware.UnreadNotificationsMiddleware',
    'user.middleware.VerificationRequiredMiddleware',
]

# Add WhiteNoise middleware only in production (when DEBUG is False)
if not DEBUG:
    MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Project URL configuration
ROOT_URLCONF = 'everything_about_sufism.urls'

# Template engine configuration
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
                'django.template.context_processors.csrf',
            ],
        },
    },
]

# Entry point for WSGI-compatible web servers to run the application.
WSGI_APPLICATION = 'everything_about_sufism.wsgi.application'

# -----------------------------------------------------------------------------
# Database Configuration
# -----------------------------------------------------------------------------

# Check if DATABASE_URL is defined first, then configure accordingly
database_url = os.getenv("DATABASE_URL")

# If DATABASE_URL is set, use PostgreSQL
if database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url, conn_max_age=600)
    }

# If DATABASE_URL is not set, use SQLite
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# -----------------------------------------------------------------------------
# Password Validation for ensuring strong passwords in user authentication
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'  # Define the language code for this installation.
TIME_ZONE = 'UTC'  # Define the time zone for this project.
USE_I18N = True  # Enable Django’s internationalization framework.
USE_L10N = True  # Format dates and numbers according to the current locale.
USE_TZ = True  # Enable timezone support.

# -----------------------------------------------------------------------------
# Static Files (CSS, JavaScript, Images)
# -----------------------------------------------------------------------------

# URL for static files
STATIC_URL = '/static/'

# Directory where collected static files are stored
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional locations for static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# If not in DEBUG mode (production), use WhiteNoise for optimized static file handling
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -----------------------------------------------------------------------------
# Media Files
# -----------------------------------------------------------------------------

# Media URL (same for both local and Cloudinary environments)
MEDIA_URL = '/media/'

# Environment check: Is it LOCAL or PRODUCTION?
USE_CLOUDINARY = os.getenv('USE_CLOUDINARY', 'False') == 'True'

if USE_CLOUDINARY:
    # Cloudinary settings
    CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Local media settings
    MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------------------------------------------------------
# Default Primary Key Field Type. Use BigAutoField for primary keys.
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------------
# Third-Party App Settings
# -----------------------------------------------------------------------------

# Override default Django message tags to use Bootstrap-compatible classes.
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Configure Crispy Forms to use Bootstrap 5 for form rendering.
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Custom color palette for CKEditor to ensure consistent styling across content
custom_color_palette = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
]

# CKEditor 5 Settings for rich text editing
CKEDITOR_5_USER_LANGUAGE = True

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', 'bulletedList',
            'numberedList', 'blockQuote', 'imageUpload',
        ],
        'language': 'en',
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3', '|',
            'bulletedList', 'numberedList', '|', 'blockQuote',
        ],
        'toolbar': [
            'heading', '|', 'outdent', 'indent', '|', 'bold', 
            'italic', 'link', 'underline', 'strikethrough', 
            'code', 'subscript', 'superscript', 'highlight', '|',
            'codeBlock', 'sourceEditing', 'insertImage', 
            'bulletedList', 'numberedList', 'todoList', '|',
            'blockQuote', 'imageUpload', '|', 'fontSize', 
            'fontFamily', 'fontColor', 'fontBackgroundColor',
            'mediaEmbed', 'removeFormat', 'insertTable',
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative', '|', 'imageStyle:alignLeft',
                'imageStyle:alignRight', 'imageStyle:alignCenter',
                'imageStyle:side', '|',
            ],
            'styles': [
                'full', 'side', 'alignLeft', 'alignRight', 'alignCenter',
            ],
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells', 
                'tableProperties', 'tableCellProperties',
            ],
            'tableProperties': {
                'borderColors': custom_color_palette,
                'backgroundColors': custom_color_palette,
            },
            'tableCellProperties': {
                'borderColors': custom_color_palette,
                'backgroundColors': custom_color_palette,
            },
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 
                 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 
                 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 
                 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 
                 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
            ],
        },
        'language': 'en',
    },
    'list': {
        'properties': {
            'styles': True, 'startIndex': True, 'reversed': True,
        },
    },
}

# -----------------------------------------------------------------------------
# Authentication Backends, including a custom email-based backend
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'user.auth_backends.EmailBackend',
]

# -----------------------------------------------------------------------------
# Email Configuration
# -----------------------------------------------------------------------------

# Email configuration settings loaded from environment variables
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Contact email addresses, separated by commas in the .env file
CONTACT_EMAILS = os.getenv('CONTACT_EMAILS', '').split(',')

# Ensure critical email settings are set.
if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    raise ValueError(
        'EMAIL_HOST_USER and EMAIL_HOST_PASSWORD must be set as environment variables.'
    )

# -----------------------------------------------------------------------------
# Login Settings
# -----------------------------------------------------------------------------

# URL to redirect users to for login
LOGIN_URL = '/user/login/'

# URL to redirect users to after a successful login
LOGIN_REDIRECT_URL = '/'

# -----------------------------------------------------------------------------
# Security settings for production: control cookie and security-related flags
# -----------------------------------------------------------------------------

# Set flags based on environment (DEBUG = True for local, False for prod)
CSRF_COOKIE_SECURE = False if DEBUG else True
SESSION_COOKIE_SECURE = False if DEBUG else True
SECURE_BROWSER_XSS_FILTER = False if DEBUG else True
SECURE_CONTENT_TYPE_NOSNIFF = False if DEBUG else True
SECURE_SSL_REDIRECT = False if DEBUG else True
SESSION_COOKIE_HTTPONLY = False if DEBUG else True

# Security headers active only in production
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # Enforces HTTPS for 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Enforces HTTPS for subdomains
    SECURE_HSTS_PRELOAD = True  # Adds site to HSTS preload list

    X_FRAME_OPTIONS = 'DENY'  # Prevents site from being embedded in iframe
    X_CONTENT_TYPE_OPTIONS = 'nosniff'  # Prevents content type sniffing

# -----------------------------------------------------------------------------
# Basic Logging Configuration
# -----------------------------------------------------------------------------

# Logs WARNING and above messages to the console, suitable for all environments
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
