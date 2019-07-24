run:
	docker run --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log kerkoapp

index:
	docker run --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log kerkoapp flask kerko index

clean:
	docker run --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log kerkoapp flask kerko clean

build:
	docker build -t kerkoapp ./

shell:
	docker run -it --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log kerkoapp bash

publish:
	git commit -m kerkoapp`git describe --tags --abbrev=0`
	docker tag kerkoapp retorquere/kerkoapp:`git describe --tags --abbrev=0`
	docker push retorquere/kerkoapp:`git describe --tags --abbrev=0`
