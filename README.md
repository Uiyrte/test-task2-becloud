# test-task2-becloud

REST API для управления задачами

## Стек

Python 3.11+, FastAPI, SQLAlchemy, SQLite.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Для разработки и тестов:

```bash
pip install -r requirements-dev.txt
```

## Запуск

```bash
uvicorn app.main:app --reload
```

API будет доступно на `http://127.0.0.1:8000`, документация Swagger — на `http://127.0.0.1:8000/docs`.

БД задаётся через `DATABASE_URL` (по умолчанию — SQLite).

## Тесты

```bash
pytest
```
