"""
WSGI config for notedown project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'notedown.productionsettings'

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'notedown'))
virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/venv/'

os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv,
                                              'lib/python3.3/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except:
    pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notedown.productionsettings")

application = get_wsgi_application()
