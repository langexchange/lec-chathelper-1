DOCKER_USERNAME ?= narutosimaha
APPLICATION_NAME ?= lec-chathelper-1
 
build:
	docker build --tag ${DOCKER_USERNAME}/${APPLICATION_NAME} .

front:
	docker-compose -f docker-compose-frontend.yml up -d --force-recreate --remove-orphans
	docker exec lec-web /etc/nginx/script.sh
	(cd ./lec_chathelper/static && make devserver)

only-front:
	(cd ./lec_chathelper/static && make devserver)

down:
	docker-compose -f docker-compose-frontend.yml down

backend:
	docker-compose -f docker-compose-frontend.yml up -d --force-recreate
