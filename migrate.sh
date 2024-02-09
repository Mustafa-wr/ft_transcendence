#!/bin/bash

python -m pip install Pillow

sleep 5

echo "Running migrate.sh script..."

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /code/localhost.key \
    -out /code/localhost.crt \
    -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/CN=localhost"

cp localhost.crt /code/project/certs/localhost.crt
cp localhost.key /code/project/certs/localhost.key

python project/manage.py makemigrations myapp --noinput
python project/manage.py migrate --noinput

# Collect static files
python project/manage.py collectstatic --noinput

# Start the server with SSL support
python project/manage.py runsslserver 0.0.0.0:8000 --cert /code/localhost.crt --key /code/localhost.key

echo "SSL enabled. Starting the server..."
