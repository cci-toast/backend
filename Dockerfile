FROM python:3

WORKDIR /usr/src/app

ADD app/requirements.txt /usr/src/app

RUN pip install -r requirements.txt

ADD app/clients /usr/src/app

CMD gunicorn django_app.wsgi:application --bind 0.0.0.0:$PORT