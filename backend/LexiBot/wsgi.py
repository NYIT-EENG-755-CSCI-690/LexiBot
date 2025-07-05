"""
WSGI config for LexiBot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LexiBot.settings')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

application = get_wsgi_application()


# Serve frontend_dist for index.html
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'backend', 'frontend_dist'), index_file=True)

# Serve assets (like /static/assets/*.css or *.js)
application.add_files(
    os.path.join(BASE_DIR, 'backend', 'frontend_dist', 'assets'),
    prefix='static/assets/')

# # Serve React static files directly
# application = WhiteNoise(application, 
#     root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'frontend_dist'), 
#     index_file=True)

# # Also tell WhiteNoise to serve the nested 'static' directory
# application.add_files(
#     os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'frontend_dist', 'static'),
#     prefix='static/')
