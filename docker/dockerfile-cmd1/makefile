## Makefile
build:
	docker build -t cmd1 .
run:
	docker run -it -d -p 8000:80 cmd1
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:make 
	docker rmi $$(docker images -q)