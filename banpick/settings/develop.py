from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!9$ka^)4dmf^)id=p_4z#44jj+)f30zhnkdc4@iwy$pte_1l=o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
