try:
	docker-compose up --build

start_server:
	docker-compose up --build -d

stop_server:
	docker-compose down