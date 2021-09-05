from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['137.184.25.201','localhost','127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':get_secret('DB_NAME'),
        'USER':get_secret('USER'),
        'PASSWORD':get_secret('PASSWORD'),
        'HOST':'localhost',
        'PORT':'5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#config para uso de mail
EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER=get_secret('EMAIL')
EMAIL_HOST_PASSWORD=get_secret('EMAILPASS')
EMAIL_PORT=587