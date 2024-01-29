FROM python:3.9

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install django-crispy-forms \
    && pip install crispy-bootstrap4 \
    && pip install requests \
    && pip install psycopg2-binary \
    && pip install django-cors-headers \
	&& pip install django-debug-toolbar

# Copy the migrate.sh script into the container
COPY migrate.sh /code/migrate.sh

# Make the script executable
RUN chmod +x /code/migrate.sh

# Run migrations before starting the server
# RUN /code/migrate.sh

# Copy the rest of your project files
COPY . /code/

RUN rm -rf /code/migrations

RUN dos2unix migrate.sh

CMD ["bash", "migrate.sh"]
