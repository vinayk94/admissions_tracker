import os
from .base import *
import logging
from django.db import connections
from django.db.utils import OperationalError
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = ['admissions-tracker.onrender.com',  'localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': 0,  # disable persistent connections

    }
}

DISABLE_CONNECTION_CHECKS = True

MIDDLEWARE = [
    'admissions_tracker.middleware.ThreadLocalMiddleware',

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
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'

# Static files
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

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
        'level': 'DEBUG',
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


logger = logging.getLogger(__name__)

# Test S3 connection
def check_s3_connection():
    try:
        # Attempt to upload a small file to S3
        test_file_name = "test_s3_connection.txt"
        test_file_content = ContentFile("This is a test file for S3 connection.")
        default_storage.save(test_file_name, test_file_content)
        logger.info("S3 connection is successful.")
    except Exception as e:
        logger.error(f"S3 connection failed: {e}")

check_s3_connection()



