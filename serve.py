import os
import sys

# Path to the project root (where manage.py lives)
BASE_DIR = os.path.dirname(__file__)

# Add 'backend' to Python path so LexiBot module can be imported
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))

# Set Django settings module explicitly (only needed if not already set in wsgi.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LexiBot.settings')

from LexiBot.wsgi import application
from waitress import serve

if __name__ == '__main__':
    print("Starting Waitress server on http://127.0.0.1:8000...")
    # serve(application, host='127.0.0.1', port=8000)
    serve(application, host='0.0.0.0', port=8000)