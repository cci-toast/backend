# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

COPY app/requirements.txt /tmp/
# install dependencies
RUN pip install -r /tmp/requirements.txt

# copy project
COPY . .

# add and run as non-root user
RUN adduser -D toastuser
USER toastuser