
FROM python:3.9

WORKDIR /code


COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install django-crispy-forms

RUN pip install django-crispy-bootstrap


COPY . /code/

cmd ["python", "manage.py", "runserver", "0.0.0.0:8000"]