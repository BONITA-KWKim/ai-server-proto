# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
import os
from .base import *

SECRET_KEY = 'yhq!ci3tvqedk!wi8fkg&o4%=y*+u2y9q&5gb07%+7-2(z+2lv'

ALLOWED_HOSTS = ['127.0.0.1',
                 'localhost']

DEBUG = True

WSGI_APPLICATION = 'ai_server_proto.wsgi.debug.application'
