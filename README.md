# Delivery Service

Сервис доставки на FastAPI. Пользователь регистрирует посылку, а её стоимость асинхронно рассчитывает Celery worker через RabbitMQ. В проекте также есть аналитика стоимости, RAG-поддержка и централизованное логирование.

## Возможности

- Регистрация и просмотр посылок с изоляцией по cookie-сессии.
- Асинхронная регистрация: API публикует задачу в RabbitMQ, а Celery worker получает курс USD/RUB, рассчитывает стоимость и сохраняет результат.
- Кэширование курса ЦБ РФ в Redis.
- PostgreSQL для посылок, MongoDB для журнала расчётов, Qdrant для базы знаний поддержки.
- AI-поддержка на базе embeddings, Qdrant и YandexGPT.
- Логирование прикладных событий через Loguru в консоль и файл.


## Технологии

- Python 3.13, FastAPI, Uvicorn
- Celery и RabbitMQ
- PostgreSQL, SQLAlchemy Async, Alembic
- Redis, MongoDB, Qdrant
- Sentence Transformers, YandexGPT
- Loguru, Pytest

## Быстрый запуск

### 1. Требования

- Python 3.13
- Poetry
- Docker Desktop

### 2. Установить зависимости

```powershell
poetry install
```

В `.env` обязательно укажите реальные значения `YANDEX_API_KEY` и `YANDEX_FOLDER_ID`, если планируете использовать endpoint `/support`.

### 3. Запустить инфраструктуру и миграции

```powershell
docker compose up -d
poetry run alembic upgrade head
```

### 4. Запустить API

```powershell
poetry run uvicorn app.main:app --reload
```

API будет доступен по адресу `http://127.0.0.1:8000`, интерактивная документация — `http://127.0.0.1:8000/docs`.

### 5. Запустить Celery worker

В отдельном терминале:

```powershell
poetry run celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo
```

`--pool=solo` необходим для локального запуска worker-а в Windows.

## Проверка асинхронной регистрации

Отправьте запрос:

```powershell
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

$body = @{
    name = "Headphones"
    weight = 2
    type = "electronics"
    content_cost_usd = 100
} | ConvertTo-Json

Invoke-WebRequest `
    -Uri "http://127.0.0.1:8000/parcels" `
    -Method POST `
    -WebSession $session `
    -ContentType "application/json" `
    -Body $body
```

API ответит `202 Accepted`:

```json
{
  "status": "accepted",
  "task_id": "..."
}
```

`task_id` идентифицирует задачу Celery, а не посылку. Worker обработает сообщение, сохранит посылку с рассчитанной стоимостью, затем её можно получить той же сессией:

```powershell
(Invoke-WebRequest `
    -Uri "http://127.0.0.1:8000/parcels" `
    -WebSession $session).Content
```

Формула стоимости:

```text
(weight × 0.5 + content_cost_usd × 0.01) × usd_rub_rate
```

Результат округляется до двух знаков по правилу `ROUND_HALF_UP`.

## API

- `POST /parcels` — поставить регистрацию посылки в очередь RabbitMQ.
- `GET /parcels` — получить посылки текущей сессии; поддерживает `limit`, `offset`, `parcel_type` и `delivery_cost_calculated`.
- `GET /parcels/{parcel_id}` — получить посылку текущей сессии по ID.
- `GET /parcel-types` — получить доступные типы: `clothes`, `electronics`, `other`.
- `GET /delivery-cost/logs/summary` — получить сумму расчётов по `target_date` и `parcel_type`.
- `POST /support` — задать вопрос AI-поддержке.

Пример тела запроса для `POST /support`:

```json
{
  "question": "Как рассчитывается стоимость доставки?"
}
```

## Конфигурация

Все параметры считываются из `.env`; полный шаблон расположен в `.env.example`.

- PostgreSQL: `DATABASE_URL`, `DATABASE_ECHO`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
- Очередь и кэш: `RABBITMQ_URL`, `REDIS_URL`.
- Хранилища: `MONGO_URL`, `MONGO_DATABASE_NAME`, `QDRANT_URL`, `QDRANT_COLLECTION_NAME`.
- Внешние API: `CBR_URL`, `HTTP_TIMEOUT_SECONDS`, `YANDEX_API_KEY`, `YANDEX_FOLDER_ID`.
- Поведение: `SESSION_TTL_SECONDS`, `EXCHANGE_RATE_CACHE_TTL_SECONDS`.
- Логи: `LOG_LEVEL`, `LOG_FILE`, `LOG_ROTATION`, `LOG_RETENTION`.

Адреса локальных сервисов:

- RabbitMQ Management: `http://localhost:15672` (`guest` / `guest`)
- Qdrant dashboard/API: `http://localhost:6333/dashboard`
- PostgreSQL: `localhost:5433`
- Redis: `localhost:6379`
- MongoDB: `localhost:27017`

## Логирование

Loguru пишет прикладные события в консоль и в файл `logs/delivery-service.log` по умолчанию. В логах фиксируются запуск приложения, публикация и обработка фоновых задач, получение курса, сохранение посылки, ошибки регистрации и события RAG-ингестии.

Каталог `logs/` исключён из Git.

## Тесты

```powershell
$env:PYTHONPATH = "."
poetry run python -m pytest -q
```

Целевые unit-тесты для расчёта, курса и регистрации:

```powershell
$env:PYTHONPATH = "."
poetry run python -m pytest `
    tests/services/test_delivery_cost.py `
    tests/services/test_parcel_registration.py `
    tests/services/test_exchange_rate.py -q
```

## Структура проекта

```text
app/
├── api/           # FastAPI-роуты и зависимости
├── cache/         # подключение к Redis
├── clients/       # ЦБ РФ и Qdrant
├── db/            # PostgreSQL и MongoDB
├── models/        # ORM- и доменные модели
├── repositories/  # доступ к данным
├── services/      # бизнес-логика
├── tasks/         # Celery-задачи
├── rag/           # ingestion и обработка документов
├── sessions/      # cookie-сессии в Redis
└── logging.py     # настройка Loguru
```