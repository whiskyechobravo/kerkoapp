FROM tiangolo/meinheld-gunicorn-flask:python3.9

LABEL maintainer="kerko@whiskyechobravo.com" \
      org.opencontainers.image.source="https://github.com/whiskyechobravo/kerkoapp" \
      org.opencontainers.image.url="https://hub.docker.com/repository/docker/whiskyechobravo/kerkoapp"

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements/run.txt
