#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

#Testing
echo "Testing"
python manage.py test

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
