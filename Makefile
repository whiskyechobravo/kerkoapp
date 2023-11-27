# This Makefile contains targets for building and running the KerkoApp Docker image.

# Change IMAGE_NAME if you wish to build your own image.
IMAGE_NAME := whiskyechobravo/kerkoapp

CONTAINER_NAME := kerkoapp
MAKEFILE_DIR := $(dir $(CURDIR)/$(lastword $(MAKEFILE_LIST)))
HOST_PORT := 8080
HOST_INSTANCE_PATH := $(MAKEFILE_DIR)instance
HOST_DEV_LOG := /tmp/kerkoapp-dev-log

SECRETS := $(HOST_INSTANCE_PATH)/.secrets.toml
CONFIG := $(HOST_INSTANCE_PATH)/config.toml
DATA := $(HOST_INSTANCE_PATH)/kerko/index

#
# Running targets.
#
# These work if the image exists, either pulled or built locally.
#

help:
	@echo "Commands for using KerkoApp with Docker:"
	@echo "    make build"
	@echo "        Build a KerkoApp Docker image locally."
	@echo "    make clean_image"
	@echo "        Remove the KerkoApp Docker image."
	@echo "    make clean_kerko"
	@echo "        Run the 'kerko clean' command from within the KerkoApp Docker container."
	@echo "    make publish"
	@echo "        Publish the KerkoApp Docker image on DockerHub."
	@echo "    make run"
	@echo "        Run KerkoApp with Docker."
	@echo "    make shell"
	@echo "        Start an interactive shell within the KerkoApp Docker container."
	@echo "    make show_version"
	@echo "        Print the version that would be used if the KerkoApp Docker image was to be built."
	@echo "\nCommands related to KerkoApp development:"
	@echo "    make requirements"
	@echo "        Pin the versions of Python dependencies in requirements files."
	@echo "    make requirements-upgrade"
	@echo "        Pin the latest versions of Python dependencies in requirements files."
	@echo "    make upgrade"
	@echo "        Update Python dependencies and install the upgraded versions."

run: | $(DATA) $(SECRETS) $(CONFIG)
	docker run --name $(CONTAINER_NAME) --rm -p $(HOST_PORT):80 -v $(HOST_INSTANCE_PATH):/kerkoapp/instance -v $(HOST_DEV_LOG):/dev/log $(IMAGE_NAME)

shell:
	docker run --name $(CONTAINER_NAME) -it --rm -p $(HOST_PORT):80 -v $(HOST_INSTANCE_PATH):/kerkoapp/instance -v $(HOST_DEV_LOG):/dev/log $(IMAGE_NAME) bash

clean_kerko: | $(SECRETS) $(CONFIG)
	docker run --name $(CONTAINER_NAME) --rm -p $(HOST_PORT):80 -v $(HOST_INSTANCE_PATH):/kerkoapp/instance -v $(HOST_DEV_LOG):/dev/log $(IMAGE_NAME) flask kerko clean everything

$(DATA): | $(SECRETS) $(CONFIG)
	@echo "[INFO] It looks like you have not run the 'flask kerko sync' command. Running it for you now!"
	docker run --name $(CONTAINER_NAME) --rm -p $(HOST_PORT):80 -v $(HOST_INSTANCE_PATH):/kerkoapp/instance -v $(HOST_DEV_LOG):/dev/log $(IMAGE_NAME) flask kerko sync

$(SECRETS):
	@echo "[ERROR] You must create '$(SECRETS)'."
	@exit 1

$(CONFIG):
	@echo "[ERROR] You must create '$(CONFIG)'."
	@exit 1

#
# Building and publishing targets.
#
# These work from a clone of the KerkoApp Git repository.
#

HASH = $(shell git rev-parse HEAD 2>/dev/null)
VERSION = $(shell git describe --exact-match --tags HEAD 2>/dev/null)

publish: | .git build
ifneq ($(shell git status --porcelain 2> /dev/null),)
	@echo "[ERROR] The Git working directory has uncommitted changes."
	@exit 1
endif
ifeq ($(findstring .,$(VERSION)),.)
	docker tag $(IMAGE_NAME) $(IMAGE_NAME):$(VERSION)
	docker push $(IMAGE_NAME):$(VERSION)
	docker tag $(IMAGE_NAME) $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):latest
else
	@echo "[ERROR] A proper version tag on the Git HEAD is required to publish."
	@exit 1
endif

build: | .git
ifeq ($(findstring .,$(VERSION)),.)
	docker build -t $(IMAGE_NAME) --no-cache --label "org.opencontainers.image.version=$(VERSION)" --label "org.opencontainers.image.created=$(shell date --rfc-3339=seconds)" $(MAKEFILE_DIR)
else
	docker build -t $(IMAGE_NAME) --no-cache --label "org.opencontainers.image.revision=$(HASH)" --label "org.opencontainers.image.created=$(shell date --rfc-3339=seconds)" $(MAKEFILE_DIR)
endif

show_version: | .git
ifeq ($(findstring .,$(VERSION)),.)
	@echo "$(VERSION)"
else
	@echo "$(HASH)"
endif

clean_image: | .git
ifeq ($(findstring .,$(VERSION)),.)
	docker rmi $(IMAGE_NAME):$(VERSION)
else
	docker rmi $(IMAGE_NAME)
endif

.git:
	@echo "[ERROR] This target must run from a clone of the KerkoApp Git repository."
	@exit 1

requirements/run.txt: requirements/run.in
	pip-compile --resolver=backtracking requirements/run.in

requirements/docker.txt: requirements/run.txt requirements/docker.in
	pip-compile --resolver=backtracking requirements/docker.in

requirements/dev.txt: requirements/run.txt requirements/dev.in
	pip-compile --allow-unsafe --resolver=backtracking requirements/dev.in

requirements: requirements/run.txt requirements/docker.txt requirements/dev.txt

requirements-upgrade:
	pre-commit autoupdate
	pip install --upgrade pip pip-tools wheel
	pip-compile --upgrade --resolver=backtracking --rebuild requirements/run.in
	pip-compile --upgrade --resolver=backtracking --rebuild requirements/docker.in
	pip-compile --upgrade --allow-unsafe --resolver=backtracking --rebuild requirements/dev.in

upgrade: | requirements-upgrade
	pip-sync requirements/dev.txt

.PHONY: help run shell clean_kerko publish build show_version clean_image requirements requirements-upgrade upgrade
