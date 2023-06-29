build:
	docker build -t remote .
run:
	docker run -it -d -p 8000:8000 --name remote remote
exec:
	docker exec -it remote /bin/bash
logs:
	docker logs remote
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
