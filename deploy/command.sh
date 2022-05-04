#!/bin/bash

# Variables
NAME="DIAGNOSIS_HUB"
PROJECT_DIR="/home/app"
DJANGO_WSGI_MODULE="core.wsgi"
NUM_WORKERS=4
NUM_THREADS=4
TIMEOUT=1800
HOST=0.0.0.0
PORT=8001

# Migrations
python $PROJECT_DIR/manage.py makemigrations
python $PROJECT_DIR/manage.py migrate
python $PROJECT_DIR/manage.py flush --no-input
python $PROJECT_DIR/manage.py loaddata category
python $PROJECT_DIR/manage.py loaddata diagnosis
python $PROJECT_DIR/manage.py runserver $HOST:$PORT

# For some reason gunicorn cannot properly display Swagger documentation interface.
# Default to using development server

# # Gunicorn Command
# gunicorn $DJANGO_WSGI_MODULE:application \
# --name $NAME \
# --chdir $PROJECT_DIR \
# --workers $NUM_WORKERS \
# --timeout $TIMEOUT \
# --bind=$HOST:$PORT \
# --log-level=debug \
# --threads=$NUM_THREADS \
# --worker-class=gevent \
# --pid=$PIDFILE

