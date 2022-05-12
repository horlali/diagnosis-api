#!/bin/bash

DEPLOY_DIR="$PWD"
PROJECT_DIR="$(dirname "$DEPLOY_DIR")"
# PROJECT_DIR="/home/gideon/diagnosis-api"


python $PROJECT_DIR/manage.py makemigrations
python $PROJECT_DIR/manage.py migrate
python $PROJECT_DIR/manage.py flush --no-input
python $PROJECT_DIR/manage.py loaddata category
python $PROJECT_DIR/manage.py loaddata diagnosis
python $PROJECT_DIR/manage.py runserver
