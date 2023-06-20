build:
	docker build -t nodejs . 
run:
	docker run -d -p 8000:8000 --name nodejs nodejs
exec:
	docker exec -it nodejs /bin/bash
start:
	docker start nodejs
attach:
	docker attach nodejs
logs:
	docker logs nodejs
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
