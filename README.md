# django-ticket-api

REST API для системы управления заявками.

## Стек

- Django + DRF
- JWT (simplejwt)
-django-filter + drf-spectacular (Swagger)
- Celery + Redis
- PostgreSQL

## Запуск

```bash
docker compose up
```

Или локально:

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver &
celery -A ticket_api worker -l info
```

## API

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/v1/auth/register/` | Регистрация |
| POST | `/api/v1/auth/login/` | JWT токен |
| POST | `/api/v1/auth/refresh/` | Обновить токен |
| GET | `/api/v1/auth/me/` | Профиль |
| GET | `/api/v1/tickets/` | Список заявок |
| POST | `/api/v1/tickets/` | Создать заявку |
| GET | `/api/v1/tickets/{id}/` | Детали заявки |
| PATCH | `/api/v1/tickets/{id}/` | Обновить заявку |
| POST | `/api/v1/tickets/{id}/assign/` | Назначить исполнителя |
| POST | `/api/v1/tickets/{id}/close/` | Закрыть заявку |
| POST | `/api/v1/tickets/{id}/comments/` | Добавить комментарий |
| POST | `/api/v1/tickets/{id}/attachments/` | Загрузить вложение |
| GET | `/api/v1/tickets/statistics/` | Статистика |
| GET | `/api/docs/` | Swagger UI |

## Фильтрация

```
GET /api/v1/tickets/?status=new&priority=high&category=bug
GET /api/v1/tickets/?assignee=1
GET /api/v1/tickets/?created_after=2024-01-01
GET /api/v1/tickets/?search=ошибка
GET /api/v1/tickets/?ordering=-created_at
```

## Роли

- **user** — свои заявки, комментарии
- **manager** — все заявки, назначение, закрытие
- **admin** — всё + админка

## Лицензия

MIT
