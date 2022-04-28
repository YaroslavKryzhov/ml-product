try:
	docker-compose up --build

start_server:
	docker-compose up --build -d --force-recreate

migrations:
	echo "alembic revision --autogenerate -m "msq_$(message)"" | docker exec -i ml-product-rest-api bash

migrate:
	echo "alembic upgrade head" | docker exec -i ml-product-rest-api bash

sleep_5:
	echo "sleep 5 sec" && \
	sleep 5

build_server:
	make start_server sleep_5 && \
	make migrations message='1' sleep_5 && \
	make migrate sleep_5

stop_server:
	docker-compose down