from ..conf.util import get_server_info_value
from .base import *

SETTING_PRD_DIC = get_server_info_value("deployment")
SECRET_KEY = SETTING_PRD_DIC["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = ['*']

'''
DATABASES = {
    'default': SETTING_PRD_DIC['DATABASES']["default"]
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

