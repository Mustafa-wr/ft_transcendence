#!/bin/bash

python -m pip install Pillow

sleep 5

echo "Running migrate.sh script..."

python project/manage.py makemigrations myapp --noinput
python project/manage.py migrate --noinput

# Collect static files
python project/manage.py collectstatic --noinput

# Start the server with SSL support
python project/manage.py runsslserver 0.0.0.0:8000 --cert /code/localhost.crt --key /code/localhost.key

echo "SSL enabled. Starting the server..."
