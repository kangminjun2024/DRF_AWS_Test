"""
WSGI config for api_pjt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('<PATH_TO_MY_DJANGO_PROJECT>/hellodjango')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_pjt.settings")

application = get_wsgi_application()
