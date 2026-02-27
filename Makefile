# This Makefile aims to facilitate common development tasks (POSIX-only).

.DEFAULT_GOAL := help

MAKEFILE_DIR := $(dir $(CURDIR)/$(lastword $(MAKEFILE_LIST)))

HASH = $(shell git rev-parse HEAD 2>/dev/null)
VERSION = $(shell git describe --exact-match --tags HEAD 2>/dev/null)

# Change DOCKER_IMAGE_NAME if you wish to build your own image.
DOCKER_IMAGE_NAME := whiskyechobravo/kerkoapp
DOCKER_CONTAINER_NAME := kerkoapp

DOCKER_HOST_PORT := 8080
DOCKER_HOST_DEV_LOG := /dev/log
DOCKER_HOST_KERKOAPP_INSTANCE_PATH := $(MAKEFILE_DIR)instance
DOCKER_HOST_KERKOAPP_SECRETS_PATH := $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH)/.secrets.toml
DOCKER_HOST_KERKOAPP_CONFIG_PATH := $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH)/config.toml
DOCKER_HOST_KERKOAPP_DATA_PATH := $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH)/kerko
DOCKER_HOST_KERKOAPP_INDEX_PATH := $(DOCKER_HOST_KERKOAPP_DATA_PATH)/index

.PHONY: help
help:
	@echo "Welcome to KerkoApp!"
	@echo "Managing the KerkoApp Docker image:\n"
	@echo "    docker-image-build"
	@echo "        Build a KerkoApp Docker image locally."
	@echo "    docker-image-clean"
	@echo "        Remove the KerkoApp Docker image."
	@echo "    docker-image-publish"
	@echo "        Publish the KerkoApp Docker image on DockerHub."
	@echo "    show-version"
	@echo "        Print the version that will be used when labelling the KerkoApp Docker image."
	@echo ""
	@echo "    Notes:"
	@echo "        These targets require Docker Engine."
	@echo ""
	@echo "Running the KerkoApp Docker container:\n"
	@echo "    docker-kerko-clean"
	@echo "        Run the 'kerko clean' command in the container."
	@echo "    docker-kerko-sync"
	@echo "        Run the 'kerko sync' command in the container."
	@echo "    docker-kerko-run"
	@echo "        Serve KerkoApp with the container."
	@echo "    docker-shell"
	@echo "        Start an interactive shell in the container."
	@echo ""
	@echo "    Notes:"
	@echo "        These targets require Docker Engine."
	@echo "        Host secrets path: $(DOCKER_HOST_KERKOAPP_SECRETS_PATH)"
	@echo "        Host config path: $(DOCKER_HOST_KERKOAPP_CONFIG_PATH)"
	@echo "        Host data path: $(DOCKER_HOST_KERKOAPP_DATA_PATH)"
	@echo ""
	@echo "Development:\n"
	@echo "    requirements"
	@echo "        Pin the versions of Python dependencies in requirements files."
	@echo "    requirements-upgrade"
	@echo "        Pin the latest versions of Python dependencies in requirements files."
	@echo "    upgrade"
	@echo "        Update Python dependencies and install the upgraded versions."
	@echo ""
	@echo "    Notes:"
	@echo "        The Python virtual environment must be activated before running these targets."

.git:
	@echo "[ERROR] This target must run from a clone of the KerkoApp Git repository."
	@exit 1

.PHONY: show-version
show-version: | .git
ifeq ($(findstring .,$(VERSION)),.)
	@echo "$(VERSION)"
else
	@echo "$(HASH)"
endif

.PHONY: docker-image-build
docker-image-build: | .git
ifeq ($(findstring .,$(VERSION)),.)
	docker build -t $(DOCKER_IMAGE_NAME) --no-cache --label "org.opencontainers.image.version=$(VERSION)" --label "org.opencontainers.image.created=$(shell date --rfc-3339=seconds)" $(MAKEFILE_DIR)
else
	docker build -t $(DOCKER_IMAGE_NAME) --no-cache --label "org.opencontainers.image.revision=$(HASH)" --label "org.opencontainers.image.created=$(shell date --rfc-3339=seconds)" $(MAKEFILE_DIR)
endif

.PHONY: docker-image-clean
docker-image-clean: | .git
ifeq ($(findstring .,$(VERSION)),.)
	docker rmi $(DOCKER_IMAGE_NAME):$(VERSION)
else
	docker rmi $(DOCKER_IMAGE_NAME)
endif

.PHONY: docker-image-publish
docker-image-publish: | .git docker-image-build
ifneq ($(shell git status --porcelain 2> /dev/null),)
	@echo "[ERROR] The Git working directory has uncommitted changes."
	@exit 1
endif
ifeq ($(findstring .,$(VERSION)),.)
	docker tag $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_NAME):$(VERSION)
	docker push $(DOCKER_IMAGE_NAME):$(VERSION)
	docker tag $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_NAME):latest
	docker push $(DOCKER_IMAGE_NAME):latest
else
	@echo "[ERROR] A proper version tag on the Git HEAD is required to publish."
	@exit 1
endif

.PHONY: docker-shell
docker-shell:
	docker run --name $(DOCKER_CONTAINER_NAME) -it --rm -p $(DOCKER_HOST_PORT):80 -v $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH):/kerko/instance -v $(DOCKER_HOST_DEV_LOG):/dev/log $(DOCKER_IMAGE_NAME) bash

$(DOCKER_HOST_KERKOAPP_SECRETS_PATH):
	@echo "[ERROR] You must create '$(DOCKER_HOST_KERKOAPP_SECRETS_PATH)'."
	@exit 1

$(DOCKER_HOST_KERKOAPP_CONFIG_PATH):
	@echo "[ERROR] You must create '$(DOCKER_HOST_KERKOAPP_CONFIG_PATH)'."
	@exit 1

$(DOCKER_HOST_KERKOAPP_INDEX_PATH): | $(DOCKER_HOST_KERKOAPP_SECRETS_PATH) $(DOCKER_HOST_KERKOAPP_CONFIG_PATH)
	@echo "[INFO] Looks like the 'kerko sync' command has not been run yet. Running it for you now!"
	docker run --name $(DOCKER_CONTAINER_NAME) --rm -p $(DOCKER_HOST_PORT):80 -v $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH):/kerko/instance -v $(DOCKER_HOST_DEV_LOG):/dev/log $(DOCKER_IMAGE_NAME) flask kerko sync

# On some systems, extended privileges are required for Gunicorn to launch within the container,
# hence the use of the --privileged option below. For production use, you may want to verify whether
# this option is really required for your system, or grant finer grained privileges. See
# https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities
.PHONY: docker-kerko-run
docker-kerko-run: | $(DOCKER_HOST_KERKOAPP_INDEX_PATH) $(DOCKER_HOST_KERKOAPP_SECRETS_PATH) $(DOCKER_HOST_KERKOAPP_CONFIG_PATH)
	docker run --privileged --name $(DOCKER_CONTAINER_NAME) --rm -p $(DOCKER_HOST_PORT):80 -v $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH):/kerko/instance -v $(DOCKER_HOST_DEV_LOG):/dev/log $(DOCKER_IMAGE_NAME)

.PHONY: docker-kerko-clean
docker-kerko-clean: | $(DOCKER_HOST_KERKOAPP_SECRETS_PATH) $(DOCKER_HOST_KERKOAPP_CONFIG_PATH)
	docker run --name $(DOCKER_CONTAINER_NAME) --rm -p $(DOCKER_HOST_PORT):80 -v $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH):/kerko/instance -v $(DOCKER_HOST_DEV_LOG):/dev/log $(DOCKER_IMAGE_NAME) flask kerko clean everything --files

.PHONY: docker-kerko-sync
docker-kerko-sync: | $(DOCKER_HOST_KERKOAPP_SECRETS_PATH) $(DOCKER_HOST_KERKOAPP_CONFIG_PATH)
	docker run --name $(DOCKER_CONTAINER_NAME) --rm -p $(DOCKER_HOST_PORT):80 -v $(DOCKER_HOST_KERKOAPP_INSTANCE_PATH):/kerko/instance -v $(DOCKER_HOST_DEV_LOG):/dev/log $(DOCKER_IMAGE_NAME) flask kerko sync

requirements/run.txt: requirements/run.in
	pip-compile --resolver=backtracking requirements/run.in
	sed -i -E 's|(\s*#\s+(via\s+)?-r\s+).*/(requirements/.+\.txt)|\1\3|' requirements/run.txt

requirements/serve.txt: requirements/run.txt requirements/serve.in
	pip-compile --resolver=backtracking requirements/serve.in
	sed -i -E 's|(\s*#\s+(via\s+)?-r\s+).*/(requirements/.+\.txt)|\1\3|' requirements/serve.txt

requirements/dev.txt: requirements/run.txt requirements/dev.in
	pip-compile --allow-unsafe --resolver=backtracking requirements/dev.in
	sed -i -E 's|(\s*#\s+(via\s+)?-r\s+).*/(requirements/.+\.txt)|\1\3|' requirements/dev.txt

.PHONY: requirements
requirements: requirements/run.txt requirements/serve.txt requirements/dev.txt

# Note: The sed command works around issue https://github.com/jazzband/pip-tools/issues/2131
.PHONY: requirements-upgrade
requirements-upgrade:
	pre-commit autoupdate
	pip install --upgrade pip pip-tools
	pip-compile --upgrade --resolver=backtracking --rebuild requirements/run.in
	pip-compile --upgrade --resolver=backtracking --rebuild requirements/serve.in
	pip-compile --upgrade --allow-unsafe --resolver=backtracking --rebuild requirements/dev.in
	sed -i -E 's|(\s*#\s+(via\s+)?-r\s+).*/(requirements/.+\.txt)|\1\3|' requirements/*.txt

.PHONY: upgrade
upgrade: | requirements-upgrade
	pip-sync requirements/dev.txt
