#!/bin/bash

# Apply Django Migrations
echo "Applying Migrations"
python manage.py makemigrations

# Apply database migrations
echo "Executing migrations..."
python manage.py migrate

# Start the Django service
exec "$@"
