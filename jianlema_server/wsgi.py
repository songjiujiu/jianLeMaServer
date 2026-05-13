"""WSGI config for jianlema_server project."""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jianlema_server.settings")

application = get_wsgi_application()
