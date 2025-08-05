# Delivery Service Project

Микросервис для службы международной доставки.
Реализован на **FastAPI**, с использованием **PostgreSQL**, **Redis** и **RabbitMQ**, упакован в **Docker Compose**.

---

## 🚀 Запуск проекта

### 1. Клонировать репозиторий
```bash
git clone https://github.com/yourname/delivery-service.git
cd delivery-service
```

### 2. Создать `.env` файл
```env
DB_HOST=db
DB_PORT=5432
DB_NAME=delivery
DB_USER=postgres
DB_PASSWORD=postgres

REDIS_HOST=redis
REDIS_PORT=6379

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=rabbit
RABBITMQ_PASSWORD=rabbit

EXCHANGE_RATE_URL=https://www.cbr-xml-daily.ru/daily_json.js
```

### 3. Запустить контейнеры
```bash
docker compose up --build
```

### 4. Применить миграции
```bash
make migrate
```

### 5. Тестирование
```bash
pytest -v -s --cov
```

Сервисы:
- FastAPI → [http://localhost:8000](http://localhost:8000)
- Swagger → [http://localhost:8000/docs](http://localhost:8000/docs)
- PostgreSQL → `localhost:5432`
- Redis → `localhost:6379`
- RabbitMQ → `localhost:5672`

---

## 📌 Основные ручки API

### 1. Зарегистрировать посылку
**POST** `/parcels/`

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/parcels/   -H "Content-Type: application/json"   -d '{
    "name": "Ноутбук",
    "weight": 2.5,
    "type_id": 2,
    "parcel_price_usd": 1200
  }'
```

**Пример ответа:**
```json
{
  "id": "f1c2d3e4-5678-4321-8765-abcdef123456",
  "name": "Ноутбук",
  "weight": 2.5,
  "type_name": "электроника",
  "parcel_price_usd": 1200,
  "delivery_price_rub": "Не рассчитано",
  "created_at": "2025-08-05T15:30:00",
  "updated_at": "2025-08-05T15:30:00"
}
```

---

### 2. Получить все типы посылок
**GET** `/parcel-types/`

**Пример запроса:**
```bash
curl http://localhost:8000/parcel-types/
```

**Пример ответа:**
```json
[
  {"id": 1, "name": "одежда"},
  {"id": 2, "name": "электроника"},
  {"id": 3, "name": "разное"}
]
```

---

### 3. Получить список посылок
**GET** `/parcels/`

Поддерживает параметры:
- `page` — номер страницы (по умолчанию 1)
- `page_size` — количество записей на страницу (по умолчанию 10)
- `type_id` — фильтр по типу
- `has_price` — `true` / `false` — наличие рассчитанной стоимости

**Пример запроса:**
```bash
curl "http://localhost:8000/parcels/?page=1&page_size=5&has_price=true"
```

**Пример ответа:**
```json
{
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Куртка",
      "weight": 1.2,
      "type_name": "одежда",
      "parcel_price_usd": 100,
      "delivery_price_rub": "945.00",
      "created_at": "2025-08-05T14:10:00",
      "updated_at": "2025-08-05T14:15:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 5
}
```

---

### 4. Получить данные о посылке по ID
**GET** `/parcels/{id}/`

**Пример запроса:**
```bash
curl http://localhost:8000/parcels/123e4567-e89b-12d3-a456-426614174000/
```

**Пример ответа:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Куртка",
  "weight": 1.2,
  "type_name": "одежда",
  "parcel_price_usd": 100,
  "delivery_price_rub": "945.00",
  "created_at": "2025-08-05T14:10:00",
  "updated_at": "2025-08-05T14:15:00"
}
```

---

## 🏗 Архитектура

- **FastAPI** — основной веб-фреймворк
- **PostgreSQL** — база данных
- **Redis** — кэширование курса валют
- **RabbitMQ** — брокер сообщений для регистрации посылок
- **Alembic** — миграции
- **Pytest** — тестирование

---

## 📖 Swagger UI
Документация доступна после запуска:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📜 Лицензия
MIT License.
