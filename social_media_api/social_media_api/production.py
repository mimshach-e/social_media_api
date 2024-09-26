from .settings import *

# Production-specific settings
SECRET_KEY = os.environ.get('SECRET_KEY')