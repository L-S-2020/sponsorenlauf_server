#!/usr/bin/env bash

python manage.py migrate --noinput
python manage.py migrate --noinput --run-syncdb
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput --username leo --email leo@example.com
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 sponsorenlauf.wsgi:application
