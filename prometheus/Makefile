APACHE_URL ?= http://lec-chathelper/server-status?auto
NETWORK ?= vutl
CONTAINER_NAME ?= lec-chathelper-exporter

run:
	docker run --rm --network=${NETWORK} --name=${CONTAINER_NAME} -d -p 9117:9117 bitnami/apache-exporter \
  --scrape_uri=${APACHE_URL}

clean:
	docker rm ${CONTAINER_NAME} --force