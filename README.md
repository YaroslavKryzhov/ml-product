# ml-product v1

## Для деплоя:

### Первоначальная сборка проекта:
```bash
make build_server
```
Запускает: 
- make start_server 
- make migrations 
- make migrate

**Выполняется один раз для создания структуры базы данных**

---
### Для запуска в dev-режиме (с отображением логов в консоль)
```bash
make try
```
### В обычном режиме:
```bash
make start_server
```
### Остановка контейнеров:
```bash
make stop_server
```

---
## После запуска сервисы доступны по:

### API Swagger: localhost:8006/docs

### Интерфейс: localhost:3036

---

Contacts: https://github.com/KirillKosvintsev
