# import os
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spa.settings")
from config.celery import app as spa

__all__ = ('spa',)





