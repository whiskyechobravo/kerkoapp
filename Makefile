run:
	docker run --env-file ./.env --rm -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log kerkoapp

build:
	docker build -t kerkoapp ./

shell:
	docker run --rm -it -p 8080:80 -v `pwd`/data:/app/data -v /tmp/kerkoapp-dev-log:/dev/log kerkoapp sh

publish:
	python3 -c "with open('version.txt','r+') as f: value = int(f.read()); f.seek(0); f.write(str(value + 1))"
	git add version.txt
	git commit -m kerkoapp`cat version.txt`
	docker tag kerkoapp retorquere/kerkoapp:`cat version.txt`
	docker push retorquere/kerkoapp:`cat version.txt`
