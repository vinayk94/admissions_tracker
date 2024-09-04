import os
from .base import *
from .base import INSTALLED_APPS, MIDDLEWARE
import logging
from django.db import connections
from django.db.utils import OperationalError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

DEBUG = False  # Set to False for production

ALLOWED_HOSTS = ['admissions-tracker.onrender.com', 'localhost', '127.0.0.1']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': 0,
    }
}

DISABLE_CONNECTION_CHECKS = True

MIDDLEWARE += [
    'admissions_tracker.middleware.ThreadLocalMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

INSTALLED_APPS += [
    'storages',
    'admissions_tracker',
]

# AWS S3 configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME') # e.g., 'us-east-1'


# Static files configuration
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media files configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# WhiteNoise configuration
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email configuration 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

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
}

print(f"Running on port: {os.getenv('PORT')}")

logger = logging.getLogger(__name__)

# Test database connection
def check_db_connection():
    db_conn = connections['default']
    try:
        db_conn.cursor()
        logger.info("Database connection is successful.")
    except OperationalError:
        logger.error("Database connection failed.")

check_db_connection()

# Test S3 connection
def check_s3_connection():
    try:
        test_file_name = "test_s3_connection.txt"
        test_file_content = ContentFile("This is a test file for S3 connection.")
        default_storage.save(test_file_name, test_file_content)
        logger.info("S3 connection is successful.")
    except Exception as e:
        logger.error(f"S3 connection failed: {e}")

check_s3_connection()

# CORS configuration
CORS_ALLOW_ALL_ORIGINS = False  # For development only, restrict this in production
CORS_ALLOWED_ORIGINS = [
    "https://admissions-tracker.onrender.com",
    "http://localhost:8000",
]