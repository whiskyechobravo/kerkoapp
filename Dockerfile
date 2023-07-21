FROM python:3.11

LABEL maintainer="kerko@whiskyechobravo.com" \
      org.opencontainers.image.source="https://github.com/whiskyechobravo/kerkoapp" \
      org.opencontainers.image.url="https://hub.docker.com/repository/docker/whiskyechobravo/kerkoapp"

WORKDIR /kerkoapp
COPY . /kerkoapp

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r /kerkoapp/requirements/docker.txt

CMD ["gunicorn", "--threads", "4", "--log-level", "info", "--error-logfile", "-", "--access-logfile", "-", "--worker-tmp-dir", "/dev/shm", "--graceful-timeout", "120", "--timeout", "120", "--keep-alive", "5", "--bind", "0.0.0.0:80", "wsgi:app"]
