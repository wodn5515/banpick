from .base import *
from banpick.utils import get_server_info_value

# SECURITY WARNING: don't run with debug turned on in production!
SETTINGS_PROD_DIC = get_server_info_value("production")

DEBUG = False

SECRET_KEY = SETTINGS_PROD_DIC["SECRET_KEY"]

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default':SETTINGS_PROD_DIC['DATABASES']['default']
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('172.31.34.28', 6379)],
        },
    },
}