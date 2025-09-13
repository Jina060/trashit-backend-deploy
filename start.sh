#!/bin/bash

# Apply database migrations
echo "Applying migrations..."
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Start the server using Gunicorn
echo "Starting Gunicorn server..."
gunicorn trashit.wsgi --bind 0.0.0.0:$PORT --log-file -
