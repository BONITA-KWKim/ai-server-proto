#!/bin/bash

# Variables
PROJECT_NAME=ai_server_proto
DJANGO_ROOT=/opt/services/djangoapp
DJANGO_SRC=$DJANGO_ROOT/src
DJANGO_PRO=$DJANGO_SRC/$PROJECT_NAME
DJANGO_MANAGE=$DJANGO_PRO/manage.py

WEB_APPLICATION_01=i_eye_proto
WEB_APPLICATION_02=snippets

cd $DJANGO_PRO
export DJANGO_SETTINGS_MODULE=ai_server_proto.settings.deploy

# Collect static files
#echo "Collect static files"
#python $DJANGO_MANAGE collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
# Add application's migration
python $DJANGO_MANAGE makemigrations $WEB_APPLICATION_01
python $DJANGO_MANAGE makemigrations $WEB_APPLICATION_02
python $DJANGO_MANAGE migrate

# create super user
echo "create super user"

##########
cat << EOF > pyscript.py
#!/usr/bin/python
import django;
django.setup();
from django.contrib.auth.management.commands.createsuperuser import get_user_model;

DJANGO_DB_NAME='default'
DJANGO_SU_USERNAME='admin'
DJANGO_SU_EMAIL='admin@my.example'
DJANGO_SU_PASSWORD='admin123!'

if get_user_model().objects.filter(username=DJANGO_SU_USERNAME):
print('Super user already exists. SKIPPING...')
else:
print('Creating super user...')
get_user_model()._default_manager.db_manager(DJANGO_DB_NAME).create_superuser(username=DJANGO_SU_USERNAME, email=DJANGO_SU_EMAIL, password= DJANGO_SU_PASSWORD)
print('Super user created...')

EOF
##########

chmod 755 pyscript.py
python ./pyscript.py
rm ./pyscript.py


# test
#echo "========== $WEB_APPLICATION_01 test start"
#python $DJANGO_MANAGE test $WEB_APPLICATION_01
#echo "========== $WEB_APPLICATION_01 test end"


# start gunicorn and django
echo "start django framework"

#gunicorn --chdir /opt/services/djangoapp/src/self_receipe --bind :8000 self_receipe.wsgi:application
#gunicorn --chdir /opt/services/djangoapp/src/self_receipe --workers=2 --bind :8000 self_receipe.wsgi:application
#gunicorn --chdir /opt/services/djangoapp/src/ai_server_proto --workers=2 --bind 0.0.0.0:8000 ai_server_proto.wsgi:application
gunicorn --chdir /opt/services/djangoapp/src/ai_server_proto --workers=2 --bind 0.0.0.0:8000 ai_server_proto.wsgi.deploy:application
