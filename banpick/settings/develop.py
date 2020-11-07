from .base import *
from banpick.utils import get_server_info_value

SETTINGS_PROD_DIC = get_server_info_value("production")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SETTINGS_PROD_DIC["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': SETTINGS_PROD_DIC['DATABASES']['default']
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    }
}