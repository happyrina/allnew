all: build run k8sinit appdep appsvc getdep getsvc getpod
k8srestart: delsvc deldep appdep appsvc getdep getsvc getpod
build:
	docker build -t weathers .
run:
	docker run -it -d -p 8000:8000 --name weathers weathers
exec:
	docker exec -it weather /bin/bash
logs:
	docker logs weathers
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
k8sinit:
	docker commit weathers weathers
	docker tag weather arin222/weathers
	docker push arin222/weathers
	docker rm -f $$(docker ps -aq)
	docker rmi arin222/weathers
	docker rmi $$(docker images -q)
appdep:
	kubectl apply -f deployment.yaml
appsvc:
	kubectl apply -f service.yaml
getdep:
	kubectl get deployment
getsvc:
	kubectl get svc -o wide
getpod:
	kubectl get pod -o wide
delsvc:
	kubectl delete svc weathers
deldep:
	kubectl delete deployment weathers
