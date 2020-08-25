from .common import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.hjm87.com', 'hjm87.com']

# STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
