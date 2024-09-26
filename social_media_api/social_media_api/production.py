from .settings import *

# Production-specific settings
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')