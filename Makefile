try:
	docker-compose up --build

up:
	docker-compose up --build -d --force-recreate

migrations:
	echo "poetry run alembic revision --autogenerate" | docker exec -i ml-product-server bash

migrate:
	echo "poetry run alembic upgrade head" | docker exec -i ml-product-server bash

revert_migration:
	echo "poetry run alembic downgrade -1" | docker exec -i ml-product-server bash

sleep_5:
	echo "sleep 5 sec" && \
	sleep 5

build_server:
	make start_server sleep_5 && \
	make migrations message='1' sleep_5 && \
	make migrate sleep_5

down:
	docker-compose down
