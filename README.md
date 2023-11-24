# ml-product v0.2.1

## Для деплоя:

### Первоначальная сборка проекта: инциализация переменных окружения
```bash
make init_env
```
`init_env` создает файл `.env` с переменными окружения, копируя `.env.example`.

Выполняется один раз перед первой сборкой

---
## Для запуска:

### Для запуска в debug-режиме (с отображением логов в консоль)
```bash
make debug
```
### В фоновом режиме:
```bash
make up
```
### Остановка контейнеров:
```bash
make down
```

---
## Конфигурация приложения:

- Конфиг, используемый приложением, находится в `server/ml_api/config.py`
- `USE_CELERY = True` используется для активации функционала бэкграунд задач через RabbitMQ и Celery
- `USE_HYPEROPT = False` используется для активации функционала подбора гиперпараметров моделей через HyperOpt

## После запуска сервисы доступны по:

### API Swagger: http://localhost:443/api/v1/docs
- Содержит описание всех эндпоинтов приложения. Документация встроена в эндпоинты

### Интерфейс: http://localhost:443
- Сейчас отключен

### Канал для вебсокета: ws://localhost:443/centrifugo/connection/websocket
- Пример подключения находится в client/centrifugo_conn.html
- Для подключения к каналу нужно использовать centrifugo jwt-токен и user_id

---
### Используемые технологии:

- FastAPI: https://fastapi.tiangolo.com/
- FastApiUsers: https://fastapi-users.github.io/fastapi-users/11.0/
- Celery: https://docs.celeryq.dev/en/stable/
- bunnet: https://roman-right.github.io/bunnet/
- Centrifugo: https://centrifugal.dev/
- RabbitMQ: https://rabbitmq.com/documentation.html
- Docker: https://www.docker.com/
- Docker-compose: https://docs.docker.com/compose/
- Nginx: https://nginx.org/ru/
- Poetry: https://python-poetry.org/
- Pandas: https://pandas.pydata.org/docs/
- Scikit-Learn: https://scikit-learn.org/stable/modules/classes.html
- HyperOpt: https://hyperopt.github.io/hyperopt/

Contacts: 
- tg: @kosvintsevke
- https://github.com/KirillKosvintsev
