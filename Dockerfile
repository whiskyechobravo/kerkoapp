FROM tiangolo/meinheld-gunicorn-flask:python3.7

MAINTAINER emiliano.heyns@iris-advies.com

# USER root
# WORKDIR /app
# ADD . /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements/run.txt

#CMD ["flask", "run"]
