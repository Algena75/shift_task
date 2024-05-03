# Сервис расчёта TF/IDF
Реализация асинхронного сервиса загрузки текстового файла с расчётом индексов TF-IDF (от англ. TF — term frequency, IDF — inverse document frequency)
## Автор:
Алексей Наумов ( algena75@yandex.ru )
## Используемые технолологии:
* FastAPI
* PostgreSQL
* Asyncio
* SQLAlchemy
* Bootstrap
* Docker

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone git@github.com:Algena75/tfidf_asyncio.git
```

```
cd tfidf_asyncio
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Подготовка:
Создать в корне проекта файл `.env` (см `.env.example`) для подключения БД.
* #### для запуска проекта в контейнерах выполнить:
    ```
    docker compose -f docker-compose.yml up -d
    ```
    открыть в браузере http://127.0.0.1/
* #### для запуска проекта в терминале:
    Выполнить миграции
    ```
    alembic upgrade head
    ```
    запустить проект
    ```
    uvicorn app.main:app --reload
    ```
    открыть в браузере http://127.0.0.1:8000/
