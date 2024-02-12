FROM python:3.9

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN apt-get update && apt-get install -y dos2unix

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install django-crispy-forms \
    && pip install crispy-bootstrap4 \
    && pip install requests \
    && pip install psycopg2-binary \
    && pip install django-cors-headers \
	&& pip install django-debug-toolbar \
	&& pip install django-sslserver
    && pip install djangorestframework\
    && pip install django-otp \
    && pip install djangorestframework-simplejwt



# Copy the migrate.sh script into the container
COPY migrate.sh /code/migrate.sh

# Make the script executable
RUN chmod +x /code/migrate.sh

# Copy the SSL key and certificate into the container

# Run migrations before starting the server
# RUN /code/migrate.sh

# RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#     -keyout /code/localhost.key \
#     -out /code/localhost.crt \
#     -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/CN=localhost"


# COPY localhost.crt /code/localhost.crt
# COPY localhost.key /code/localhost.key
# Copy the rest of your project files
COPY . /code/

RUN rm -rf /code/migrations

RUN dos2unix /code/migrate.sh

CMD ["bash", "migrate.sh"]
