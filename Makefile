run:
	docker run --env-file ./.env --rm -p 8080:80 kerkoapp

build:
	docker build -t kerkoapp ./

shell:
	docker run --rm -it -p 8080:80 kerkoapp sh
