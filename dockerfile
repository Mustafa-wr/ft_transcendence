FROM python:3.9

RUN mkdir /code

WORKDIR /code


COPY requirements.txt /code/

RUN pip install --upgrade pip \
    pip install -r requirements.txt \
    pip install django-crispy-forms \
    pip install crispy-bootstrap4 \
    pip install requests \
    pip install psycopg2-binary \
    pip install django-cors-headers



# RUN python manage.py makemigrations

# RUN python manage.py migrate

COPY . /code/

CMD ["python", "./project/manage.py", "runserver", "0.0.0.0:8000"]