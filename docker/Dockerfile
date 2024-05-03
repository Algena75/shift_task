FROM python:3.10.12-slim

WORKDIR /app

COPY pyproject.toml /poetry.lock docker/server-entrypoint.sh alembic.ini README.md ./

COPY alembic/ ./alembic
COPY shift_task/ ./shift_task

RUN apt update && pip install poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install --without test --no-interaction --no-ansi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN chmod +x ./server-entrypoint.sh
