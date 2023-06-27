MAKEFILE_DIR := $(dir $(CURDIR)/$(lastword $(MAKEFILE_LIST)))
REPOSITORY = whiskyechobravo/kerkoapp
IMAGE = whiskyechobravo/kerkoapp
# Uncomment the following line to work with your local image.
# IMAGE = kerkoapp
HOST_PORT = 8080
HOST_DATA_DIR = $(MAKEFILE_DIR)data
HOST_DEV_LOG = /tmp/kerkoapp-dev-log
ENV_FILE = $(MAKEFILE_DIR).env

run:
	docker run --env-file $(ENV_FILE) --rm -p $(HOST_PORT):80 -v $(HOST_DATA_DIR):/app/data -v $(HOST_DEV_LOG):/dev/log $(IMAGE)

pull:
	docker pull $(IMAGE)

kerkosync:
	docker run --env-file $(ENV_FILE) --rm -p $(HOST_PORT):80 -v $(HOST_DATA_DIR):/app/data -v $(HOST_DEV_LOG):/dev/log $(IMAGE) flask kerko sync

kerkoclean:
	docker run --env-file $(ENV_FILE) --rm -p $(HOST_PORT):80 -v $(HOST_DATA_DIR):/app/data -v $(HOST_DEV_LOG):/dev/log $(IMAGE) flask kerko clean everything

kerkocleancache:
	docker run --env-file $(ENV_FILE) --rm -p $(HOST_PORT):80 -v $(HOST_DATA_DIR):/app/data -v $(HOST_DEV_LOG):/dev/log $(IMAGE) flask kerko clean cache

kerkocleanindex:
	docker run --env-file $(ENV_FILE) --rm -p $(HOST_PORT):80 -v $(HOST_DATA_DIR):/app/data -v $(HOST_DEV_LOG):/dev/log $(IMAGE) flask kerko clean index

kerkocleanattachments:
	docker run --env-file $(ENV_FILE) --rm -p $(HOST_PORT):80 -v $(HOST_DATA_DIR):/app/data -v $(HOST_DEV_LOG):/dev/log $(IMAGE) flask kerko clean attachments

build:
	docker build -t kerkoapp --label "org.opencontainers.image.version=`git describe --tags`" --label "org.opencontainers.image.created=`date --rfc-3339=seconds`" $(MAKEFILE_DIR)

shell:
	docker run -it --env-file $(ENV_FILE) --rm -p $(HOST_PORT):80 -v $(HOST_DATA_DIR):/app/data -v $(HOST_DEV_LOG):/dev/log $(IMAGE) bash

publish:
	docker tag kerkoapp $(REPOSITORY):`git describe --tags`
	docker push $(REPOSITORY):`git describe --tags`
	docker tag kerkoapp $(REPOSITORY):latest
	docker push $(REPOSITORY):latest
