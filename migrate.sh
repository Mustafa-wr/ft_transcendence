#!/bin/bash

python project/manage.py makemigrations myapp --noinput
python project/manage.py migrate --noinput

python project/manage.py runserver 0000:8000