FROM tiangolo/meinheld-gunicorn-flask:python3.7

MAINTAINER emiliano.heyns@iris-advies.com

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements/run.txt

