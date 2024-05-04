# Сервис просмотра информации по допуску
Реализация асинхронного сервиса с JWT аутентификацией
## Автор:
Алексей Наумов ( algena75@yandex.ru )
## Используемые технолологии:
* FastAPI
* PostgreSQL
* JWT
* Asyncio
* SQLAlchemy
* Pytest
* Docker
* Nginx
## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone git@gitlub.com:algena75/shift_task.git
```

```
cd shift_task
```

### Запуск виртуального окружения

Создание виртуального окружения:
```bash
poetry env use python3.10
```
Установка зависимостей:
```bash
poetry install --with test
```
Запуск оболочки и активация виртуального окружения (из папки проекта):
```bash
poetry shell
```
Проверка активации виртуального окружения:
```bash
poetry env list
```
## Подготовка:
Создать в корне проекта файл `.env` (см `.env.example`) для подключения БД.
При старте проекта будет создан первый суперпользователь, от имени которого можно будет создавать других пользователей и суперпользователей через Swagger документацию.
Обычный пользователь может увидеть свои данные по адресу http://127.0.0.1/users/me . К остальным эндпоинтам доступ отсутсвует. При вводе своих данных 
(`email` и `password`) по адресу http://127.0.0.1/auth/jwt/login любой пользователь получает токен для доступа к эндпоинтам.

* #### для запуска проекта в контейнерах выполнить:
    ```bash
    docker compose -f docker-compose.yml up -d
    ```
    открыть в браузере http://127.0.0.1/docs
* #### для запуска проекта в терминале:
    Выполнить миграции
    ```bash
    alembic upgrade head
    ```
    запустить проект
    ```bash
    poetry run project
    ```
    открыть в браузере http://127.0.0.1:8000/docs
