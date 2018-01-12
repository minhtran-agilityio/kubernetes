#!/bin/sh
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

/usr/local/bin/gunicorn config.wsgi:application -w 2 -b :8000 --reload
