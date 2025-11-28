# 📋 ToDoList Application

A **CLI-based task management system** built with  
**Python OOP**, **SQLAlchemy ORM**, **PostgreSQL**, **Docker**, and **Alembic migrations**.

Now fully persistent — your tasks and projects are stored in a **relational database** instead of in‑memory.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/dependency%20management-poetry-blue)](https://python-poetry.org/)
[![Database](https://img.shields.io/badge/database-PostgreSQL-316192.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/containerized-Docker-blue.svg)](https://www.docker.com/)
[![Migrations](https://img.shields.io/badge/migrations-Alembic-yellow.svg)](https://alembic.sqlalchemy.org/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 Features

### Project Management
- Create, read, update, delete projects  
- Configurable maximum number of projects  
- Word‑count validation for names/descriptions  
- Prevent duplicate names  
- View project summaries and progress  

### Task Management
- Full CRUD operations  
- Status workflow: `todo`, `in_progress`, `done`  
- Optional deadlines (`YYYY-MM-DD`, validated, must be in the future)  
- Search tasks by title/description  
- View overdue tasks  
- Project completion calculations  

### Data Validation
- Word-count constraints  
- Enum status validation  
- Date format checking  
- Custom exception hierarchy (base, repository, service)  

### Persistence Layer
- PostgreSQL relational database  
- SQLAlchemy ORM models (`Project`, `Task`)  
- Repository pattern (clean separation of DB from business logic)

### Migrations
- Alembic auto‑generation  
- Versioned schema upgrades  
- Easily reproducible database setup

### Infrastructure
- Database runs in Docker  
- Local development uses environment variables  
- Fully portable and OS‑independent  

---

## 📁 Updated Project Structure

```bash
To-Do-List/
├── todolist_app/
│   ├── cli/
│   │   └── main.py               # Entry point for CLI
│   ├── db/
│   │   ├── base.py               # SQLAlchemy Base
│   │   ├── session.py            # DB session + context manager
│   │   └── __init__.py
│   ├── models/                   # ORM models: Project, Task
│   ├── repository/               # Repository layer
│   ├── services/                 # Business logic
│   ├── utils/
│   │   ├── config.py             # Reads .env + DB URL builder
│   │   └── validators.py
│   ├── exceptions/               # Custom exceptions
│   └── alembic/                  # Alembic migrations
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
├── docker-compose.yml            # PostgreSQL in Docker
├── main.py                       # Shortcut runner
├── pyproject.toml
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.10+**
- **Poetry**
- **Docker Desktop** installed + running

---

### 2. Install Dependencies

```bash
git clone https://github.com/yourusername/To-Do-List.git
cd To-Do-List
poetry install
```

---

### 3. Setup Environment Variables

Create a file `.env` in the project root:

```bash
# App
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50

# Database
DB_USER=todouser
DB_PASSWORD=todopass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todolist_db
```

---

### 4. Start PostgreSQL in Docker

```bash
docker-compose up -d
```

Check DB is running:

```bash
docker ps
```

---

### 5. Run Database Migrations

```bash
alembic upgrade head
```

If you change models:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## 🎯 Run the Application

### Option 1 — Direct

```bash
poetry run todolist
```

### Option 2 — Inside Poetry Shell

```bash
poetry shell
todolist
```

---

## 📟 CLI Menu

```
📋 ToDo List Manager
1.  Create Project
2.  List All Projects
3.  Edit Project
4.  Delete Project
5.  Select Project
6.  Create Task
7.  List Tasks
8.  Edit Task
9.  Change Task Status
10. Delete Task
11. View Project Status
0.  Exit
```

---

## 🧪 Testing

Run all tests:

```bash
poetry run pytest -v
```

---

## 📄 License

MIT License.  
Feel free to fork, improve, and contribute!
