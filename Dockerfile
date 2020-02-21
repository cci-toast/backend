# Dockerfile

# Python version
FROM python:3.7-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET_KEY zh2w7w&rzn^0mnsfpv+^=&!d6)16!#rc#@)h^jc8n_0hx^z+b%

# Install psycopg2 dependencies
RUN apk update && \
    apk add  --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev

RUN mkdir /code
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install djangorestframework django-cors-headers

# Copy project
COPY . /code/