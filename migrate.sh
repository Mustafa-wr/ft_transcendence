#!/bin/bash

echo "Running migrate.sh script..."

python project/manage.py makemigrations myapp --noinput
python project/manage.py migrate --noinput

echo "\nMigrations completed."

python project/manage.py runserver 0.0.0.0:8000