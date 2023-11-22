try:
	#docker-compose up --build --force-recreate --remove-orphans
	docker-compose up --build -d --force-recreate
	docker-compose logs -f server

up:
	docker-compose up --build -d --force-recreate

down:
	docker-compose down

init_env:
	cp ./.env.example ./.env

data_init:
	make up sleep_5 && \
	make migrations sleep_5 && \
	make migrate

migrations:
	echo "poetry run alembic revision --autogenerate" | docker exec -i ml-product-server bash

migrate:
	echo "poetry run alembic upgrade head" | docker exec -i ml-product-server bash

revert_migration:
	echo "poetry run alembic downgrade -1" | docker exec -i ml-product-server bash

sleep_5:
	echo "sleep 5 sec" && \
	sleep 5
