# start from an official image
FROM python:3.6

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# copy our project code
COPY . /opt/services/djangoapp/src

# install our two dependencies
#RUN pip install gunicorn django djangorestframework django-filter pygments coreapi
#RUN pwd
RUN pip install -r ai_server_proto/requirements.txt

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
#CMD ["gunicorn", "--chdir", "ai_server_proto", "--bind", ":8000", "ai_server_proto.wsgi:application"]
