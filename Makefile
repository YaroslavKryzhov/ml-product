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
