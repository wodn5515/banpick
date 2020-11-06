from .base import *
from banpick.utils import get_server_info_value

# SECURITY WARNING: don't run with debug turned on in production!
SETTINGS_PROD_DIC = get_server_info_value("production")

DEBUG = False

SECRET_KEY = SETTINGS_PROD_DIC["SECRET_KEY"]

ALLOWED_HOSTS = [
    "13.209.254.130",
    "bnpk.kr"
]

DATABASES = {
    'default':SETTINGS_PROD_DIC['DATABASES']['default']
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(SETTINGS_PROD_DIC['CHANNEL_LAYERS']['hosts'], 6379)],
        },
    },
}