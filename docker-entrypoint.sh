#!/bin/bash
# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Create base instances
echo "Creating base instances"
python manage.py create_base_instances

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
