export CURRENT_UID = $(id -u)

start:
	docker-compose up -d

restart:
	docker-compose stop
	docker-compose rm
	docker-compose up -d
