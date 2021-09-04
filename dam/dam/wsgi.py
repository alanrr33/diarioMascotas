"""
WSGI config for dam project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#cambiar de vuelta a local una vez terminado el deploy 'dam.settings.local'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dam.settings.prod')

application = get_wsgi_application()
