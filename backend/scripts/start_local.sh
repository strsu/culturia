#!/usr/bin/env bash

mkdir -p log

python manage_local.py makemigrations
python manage_local.py migrate
python manage_local.py collectstatic --noinput --verbosity 0

service cron start
python manage_local.py crontab add
python manage_local.py runserver 0.0.0.0:8000