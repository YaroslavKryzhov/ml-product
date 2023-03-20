# ml-product v0.2.1

## Для деплоя:

### Первоначальная сборка проекта: инциализация окружения и базы данных
```bash
make init_env
make data_init
```
`init_env` создает файл `.env` с переменными окружения.
`data_init` запускает миграции базы данных, что позволяет создать нужные таблицы.

Выполняется один раз перед первой сборкой

---
## Для запуска:

### Для запуска в dev-режиме (с отображением логов в консоль)
```bash
make try
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
## После запуска сервисы доступны по:

### API Swagger: http://localhost:6060/api/v1/docs

### Интерфейс: http://localhost:6060

### Канал для вебсокета: ws://localhost:6060/centrifugo/connection/websocket

---

Contacts: https://github.com/KirillKosvintsev

