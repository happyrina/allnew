build:
	docker build -t myreact .
run:
	docker run -p 8000:80 myreact
exec:
	docker exec -it myreact /bin/bash
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)