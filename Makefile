REPOSITORY = whiskyechobravo/kerkoapp
IMAGE = kerkoapp # local
IMAGE = whiskyechobravo/kerkoapp:0.3alpha1-18-gf8b5603 # remote

run:
	docker run --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log $(IMAGE)

pull:
	docker pull $(IMAGE)

index:
	docker run --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log $(IMAGE) flask kerko index

clean:
	docker run --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log $(IMAGE) flask kerko clean

build:
	docker build -t kerkoapp --label "org.opencontainers.image.version=`git describe --tags`" --label "org.opencontainers.image.created=`date --rfc-3339=seconds`" ./

shell:
	docker run -it --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log $(IMAGE) bash

publish:
	docker tag kerkoapp $(REPOSITORY):`git describe --tags`
	docker push $(REPOSITORY):`git describe --tags`
	docker tag kerkoapp $(REPOSITORY):latest
	docker push $(REPOSITORY):latest
