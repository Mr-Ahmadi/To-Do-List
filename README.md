# 📋 ToDoList Application

A **CLI-based task management system** built with
**Python OOP**, **SQLAlchemy ORM**, **PostgreSQL**, **Docker**, and **Alembic**.

The application now uses a **fully persistent PostgreSQL database**, replacing the previous in-memory storage model.

**NEW:** Automated overdue-task closure through **scheduled commands** (Cron or Python scheduler).

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

* Create, read, update, and delete projects
* Configurable project-limit settings
* Name/description validation and duplicate checks
* View summaries and project-level progress

### Task Management

* Full task CRUD
* Status workflow: `todo`, `in_progress`, `done`
* Optional future-dated deadlines (`YYYY-MM-DD`)
* Search tasks by title or description
* View overdue tasks
* Automatic project progress calculation

### Scheduled Automation ✨ **NEW**

* **Automatic closure of overdue tasks**
* Command: `tasks:autoclose-overdue`
* Can run:

  * Manually (CLI)
  * Automatically (Python scheduler)
  * Automatically (Cron, every 15 minutes)

### Data Validation

* Word-count constraints
* Enum-based status validation
* Date-format enforcement
* Layered custom exception hierarchy

### Persistence Layer

* PostgreSQL backend
* SQLAlchemy ORM models
* Clean repository pattern for DB access

### Migrations

* Alembic auto-generated migrations
* Versioned schema updates
* Repeatable, portable DB setup

### Infrastructure

* PostgreSQL via Docker
* Environment-variable configuration
* Fully portable across OS environments

---

## 📁 Project Structure

```bash
To-Do-List/
├── todolist_app/
│   ├── cli/
│   │   ├── console.py
│   │   └── __init__.py
│   ├── commands/
│   │   ├── autoclose_overdue.py
│   │   └── __init__.py
│   ├── scheduler/
│   │   ├── autoclose_runner.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── utils/
│   │   ├── config.py
│   │   └── validators.py
│   ├── exceptions/
│   └── alembic/
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
├── docker-compose.yml
├── run_scheduler.sh
├── logs/
│   └── scheduler.log
├── main.py
├── pyproject.toml
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Requirements

* Python **3.10+**
* **Poetry**
* **Docker Desktop** (running)

---

### 2. Install Dependencies

```bash
git clone https://github.com/Mr-Ahmadi/To-Do-List.git
cd To-Do-List
poetry install
```

To enable scheduled tasks:

```bash
poetry add schedule
```

---

### 3. Configure Environment Variables

Create a `.env` file in the project root:

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

### 4. Start PostgreSQL (Docker)

```bash
docker-compose up -d
```

Verify:

```bash
docker ps
```

---

### 5. Run Migrations

```bash
alembic upgrade head
```

After any model changes:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## 🎯 Running the Application

### Option 1 — Interactive CLI

```bash
poetry run python main.py
```

OR:

```bash
poetry shell
python main.py
```

### Option 2 — Direct Command Execution

```bash
poetry run todolist tasks:autoclose-overdue
```

---

## 📟 CLI Menu (Interactive Mode)

```
📋 ToDo List Manager
1. Create Project
2. List All Projects
3. Edit Project
4. Delete Project
5. Select Project
6. Create Task
7. List Tasks
8. Edit Task
9. Change Task Status
10. Delete Task
11. View Project Status
0. Exit
```

---

## ⏰ Scheduled Task Automation

### What It Does

The `tasks:autoclose-overdue` command automatically:

* Finds all tasks where `deadline < now` and `status != done`
* Sets `status = done`
* Updates `closed_at = now()`

### Run Scheduler Manually

```bash
poetry run python -m todolist_app.scheduler.autoclose_runner
```

This runs every **15 minutes** in a continuous loop.

---

## 🔁 Running with Cron

### Step 1: Create Script

`run_scheduler.sh`:

```bash
#!/bin/bash
cd /path/to/To-Do-List || exit
POETRY_PATH=$(command -v poetry)
$POETRY_PATH run python -m todolist_app.scheduler.autoclose_runner >> logs/scheduler.log 2>&1
```

### Step 2: Make Executable

```bash
chmod +x run_scheduler.sh
```

### Step 3: Add Cron Job

```bash
crontab -e
```

Add:

```bash
*/15 * * * * /path/to/To-Do-List/run_scheduler.sh
```

### Step 4: Verify

```bash
crontab -l
tail -f logs/scheduler.log
```

---

## 🧪 Testing

```bash
poetry run pytest -v
```

---

## 🛠️ Troubleshooting

### `ModuleNotFoundError: No module named 'schedule'`

```bash
poetry add schedule
```

### Scheduler not running via Cron

* Check `crontab -l`
* Check logs: `cat logs/scheduler.log`
* Verify script path and permissions
* Confirm Poetry path with `which poetry`

### Database connection issues

Check Docker:

```bash
docker ps
```

Start if needed:

```bash
docker-compose up -d
```

---

## 📄 License

MIT License
Feel free to fork, contribute, and improve!
