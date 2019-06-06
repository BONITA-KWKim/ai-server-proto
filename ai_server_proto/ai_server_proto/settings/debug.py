# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

from .base import *

SECRET_KEY = 'yhq!ci3tvqedk!wi8fkg&o4%=y*+u2y9q&5gb07%+7-2(z+2lv'

ALLOWED_HOSTS = ['127.0.0.1',
                 'localhost']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
