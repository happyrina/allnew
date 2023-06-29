build:
	docker build -t weather .
run:
	docker run -it -d -p 8000:8000 --name weather weather
exec:
	docker exec -it weather /bin/bash
logs:
	docker logs weather
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rim:
	docker rmi $$(docker images -q)
