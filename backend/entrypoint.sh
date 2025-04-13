#!/bin/bash
set -e

# Wait for MySQL to be available
echo "Waiting for MySQL..."
until nc -z -v -w30 host.docker.internal 3306
do
  echo "Waiting for database connection..."
  sleep 5
done

# Run DB setup
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json

# Start dev server
exec python manage.py runserver 0.0.0.0:8000
