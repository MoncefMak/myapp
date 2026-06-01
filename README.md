# authservice

A small, production-minded **REST API for user accounts and JWT authentication**, built with Django 5 and Django REST Framework. It ships with a custom email-login user model, token auth, object-level permissions, OpenAPI docs, and CI.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14-A30000)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)

## Features

- **Custom user model** with a UUID primary key and **email as the login identifier** (`accounts.User`).
- **JWT authentication** (access/refresh) via `djangorestframework-simplejwt`, with custom claims (`username`, `email`) embedded in the token.
- **Registration** endpoint that hashes passwords and enforces Django's password validators.
- **Object-level permissions**: a user can only read/update their own profile.
- **OpenAPI 3 schema + Swagger UI** via `drf-spectacular`.
- **Tested**: model + API test suite (registration, auth, permissions, negative paths).
- **CI**: GitHub Actions runs migrations, deploy checks, and the full test suite against PostgreSQL.

## Tech stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11 |
| Framework | Django 5.0, Django REST Framework 3.14 |
| Auth | JWT (simplejwt) |
| Database | PostgreSQL |
| API docs | drf-spectacular (OpenAPI 3 / Swagger UI) |
| CI | GitHub Actions |

## Project layout

```
authservice/                 # repo root
├─ .github/workflows/main.yml
└─ authservice/              # Django project (manage.py lives here)
   ├─ manage.py
   ├─ requirements.txt
   ├─ .env.example
   ├─ accounts/              # custom User model + manager (the domain app)
   ├─ api/                   # DRF views, serializers, permissions, urls
   └─ authservice/           # settings, root urls, wsgi/asgi
```

## Getting started

> Requires Python 3.11+ and a running PostgreSQL instance.

```bash
# 1. clone and enter the Django project
cd authservice

# 2. create a virtualenv and install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. configure environment
cp .env.example .env
# then edit .env — at minimum set SECRET_KEY (generate one with the command below)
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"

# 4. migrate and run
python manage.py migrate
python manage.py createsuperuser   # prompts for email (the login field)
python manage.py runserver
```

API docs are then available at **http://127.0.0.1:8000/api/docs/** (Swagger UI).

## API

Base path: `/api/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/users/` | — | Register a new user |
| `GET` | `/api/users/{id}/` | JWT (owner) | Retrieve own profile |
| `PATCH` / `PUT` | `/api/users/{id}/` | JWT (owner) | Update own profile |
| `POST` | `/api/login/` | — | Obtain access + refresh tokens |
| `POST` | `/api/login/refresh/` | — | Refresh an access token |
| `GET` | `/api/schema/` | — | OpenAPI 3 schema |
| `GET` | `/api/docs/` | — | Swagger UI |

### Examples

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "Str0ngPass!42"}'

# Log in -> { "access": "...", "refresh": "..." }
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "Str0ngPass!42"}'

# Update own profile (replace TOKEN and ID)
curl -X PATCH http://127.0.0.1:8000/api/users/<ID>/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice2"}'
```

## Running the tests

```bash
python manage.py test
```

## Security notes

- Secrets are read from environment variables (`django-environ`); **no secrets are committed** — see `.env.example`.
- Production security headers (HSTS, secure cookies, SSL redirect) are enabled automatically when `DEBUG` is off.
- Passwords are hashed and validated against Django's `AUTH_PASSWORD_VALIDATORS`.
