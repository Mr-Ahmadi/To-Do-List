Here is a **clean, professional, production‑style README.md** written specifically for *your exact project structure*, fully reflecting:

- FastAPI backend  
- PostgreSQL + SQLAlchemy  
- Repository/Service architecture  
- CLI  
- Scheduler  
- Alembic migrations  
- Pytest test suite  
- No front-end client (API‑only server)  

Everything is concise, polished, and ready for GitHub / university submission.

---

# README.md

# ToDoList App (FastAPI + PostgreSQL + SQLAlchemy)

A modular, scalable **Task & Project Management API** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM**, and **Pydantic**.  
Includes a full **repository–service architecture**, **CLI tools**, **scheduled background jobs**, and a complete **unit-test suite** with HTML coverage reports.

This project was developed as part of a multi‑phase backend engineering task focusing on API design, data modeling, validation, CLI tooling, and database-backed service layers.

---

## Features

### ✓ RESTful API (FastAPI)
- CRUD for **Projects**
- CRUD for **Tasks**
- Status management (`todo`, `doing`, `done`)
- Deadline validation (ISO date format)
- List, filter, search, mark-done, overdue detection

### ✓ PostgreSQL + SQLAlchemy ORM
- Normalized relational schema  
- Programmatic DB sessions  
- Alembic migrations for schema evolution

### ✓ Repository–Service Architecture
Clean separation of concerns:

- `repositories/` → low-level DB operations  
- `services/` → business logic & validation  
- `managers/` → high-level orchestration  
- `api/routers/` → HTTP layer  

### ✓ CLI Tools
Run admin commands directly from terminal:

```
poetry run todolist --help
```

Includes:

- Initialize data
- Close overdue tasks
- Project/task listing

### ✓ Scheduler
Automatic daily job to **autoclose overdue tasks**:

```
./run_scheduler.sh
```

### ✓ Test Suite (Pytest)
All key layers fully tested:

- Managers  
- Services  
- Validators  
- CLI  
- Config  

Coverage report available in `htmlcov/`.

---

## Project Structure

```
todolist_app/
├── api/                   # FastAPI application
│   ├── main.py
│   ├── routers/
│   └── schemas/
├── cli/                   # Command-line interface
├── commands/              # CLI commands
├── db/                    # Database engine, session, base ORM
├── models/                # SQLAlchemy ORM models
├── repositories/          # DB access layer
├── services/              # Business logic
├── managers/              # High-level wrappers
├── utils/                 # Config, validators
├── scheduler/             # Background scheduled job
└── alembic/               # Migrations
```

Other top-level files:

```
main.py                   # Entry point to API
run_api.sh                # Run FastAPI server
run_scheduler.sh          # Run scheduler
api_tests.http            # REST client manual tests
tests/                    # Pytest suite
htmlcov/                  # Coverage HTML output
docker-compose.yml        # PostgreSQL + API optional
pyproject.toml            # Poetry config
requirements.txt          # Pinned dependencies
```

---

## Requirements

- Python 3.12+
- Poetry
- PostgreSQL 14+
- Docker (optional, for DB)

---

## Installation

### 1) Clone the repository

```
git clone <repo-url>
cd todolist-app
```

### 2) Install dependencies

```
poetry install
```

### 3) Set up environment variables

Create `.env`:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/todolist
MAX_PROJECTS=10
MAX_TASKS=100
```

(or use Docker + provided `docker-compose.yml`)

### 4) Run migrations

```
poetry run alembic upgrade head
```

---

## Running the API Server

```
./run_api.sh
```

Equivalent:

```
poetry run uvicorn todolist_app.api.main:app --reload --port 8001
```

API available at:

```
http://localhost:8001/api
```

Interactive docs:

```
http://localhost:8001/docs
```

---

## Running the Scheduler

Automatic overdue cleanup:

```
./run_scheduler.sh
```

---

## Running the CLI

Command:

```
poetry run todolist
```

---


## Development Notes

- Validation uses Pydantic models and custom validators.
- Fully typed with Python type hints.
- Service layer protected with application-specific exceptions (`service_exceptions.py`).
- Repository errors wrapped and re-raised cleanly.
- Database access via `SessionLocal` factory.

---

## License

MIT License.

---
