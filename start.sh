#!/bin/bash

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the server with Gunicorn
gunicorn trashit.wsgi
