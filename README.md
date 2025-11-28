# 📋 ToDoList Application

A **CLI-based task management system** built with  
**Python OOP**, **SQLAlchemy ORM**, **PostgreSQL**, **Docker**, and **Alembic migrations**.

Now fully persistent — your tasks and projects are stored in a **relational database** instead of in‑memory.

**NEW**: Automated overdue task closure with **scheduled commands** (via Cron or Python scheduler).

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

### Scheduled Task Automation ✨ **NEW**

- **Automatic closure of overdue tasks**  
- Command: `tasks:autoclose-overdue` (sets `status=done`, `closed_at=now`)  
- Can be triggered:
  - Manually via CLI  
  - Automatically via Python scheduler (`schedule` library)  
  - Automatically via Cron Job (runs every 15 minutes)

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
│   │   ├── console.py            # Interactive CLI
│   │   └── __init__.py
│   ├── commands/                 # CLI Commands (Click-based)
│   │   ├── autoclose_overdue.py  # tasks:autoclose-overdue
│   │   └── __init__.py           # Command group registration
│   ├── scheduler/                # Scheduled task runners
│   │   ├── autoclose_runner.py   # Runs autoclose every 15 min
│   │   └── __init__.py
│   ├── db/
│   │   ├── base.py               # SQLAlchemy Base
│   │   ├── session.py            # DB session + context manager
│   │   └── __init__.py
│   ├── models/                   # ORM models: Project, Task
│   ├── repositories/             # Repository layer (TaskRepository, ProjectRepository)
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
├── run_scheduler.sh              # Shell script for Cron execution
├── logs/                         # Scheduler logs
│   └── scheduler.log
├── main.py                       # Entry point
├── pyproject.toml
├── .env
├── .gitignore
└── README.md

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.10+**
- **Poetry**
- **Docker Desktop** installed + running

---

### 2. Install Dependencies

bash
git clone https://github.com/Mr-Ahmadi/To-Do-List.git
cd To-Do-List
poetry install

If you need the scheduler (for automated overdue task closure):

bash
poetry add schedule

---

### 3. Setup Environment Variables

Create a file `.env` in the project root:

bash
# App
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50

# Database
DB_USER=todouser
DB_PASSWORD=todopass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todolist_db

---

### 4. Start PostgreSQL in Docker

bash
docker-compose up -d

Check DB is running:

bash
docker ps

---

### 5. Run Database Migrations

bash
alembic upgrade head

If you change models:

bash
alembic revision --autogenerate -m "description"
alembic upgrade head

---

## 🎯 Run the Application

### Option 1 — Interactive CLI

bash
poetry run python main.py

or

bash
poetry shell
python main.py

### Option 2 — Direct Commands

Run the autoclose command manually:

bash
poetry run todolist tasks:autoclose-overdue

---

## 📟 CLI Menu (Interactive Mode)


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

---

## ⏰ Scheduled Task Automation

### What Does It Do?

The `tasks:autoclose-overdue` command automatically:
- Finds all tasks where `deadline < now` and `status != done`
- Sets `status = done`
- Sets `closed_at = now()`

### Running the Scheduler Manually

bash
poetry run python -m todolist_app.scheduler.autoclose_runner

This will run the autoclose job **every 15 minutes** in a persistent loop.

---

### Setting Up Cron (Automated Execution)

#### Step 1: Create the Shell Script

Create `run_scheduler.sh` in the project root:

bash
#!/bin/bash
cd /path/to/To-Do-List || exit
POETRY_PATH=$(command -v poetry)
$POETRY_PATH run python -m todolist_app.scheduler.autoclose_runner >> logs/scheduler.log 2>&1

Replace `/path/to/To-Do-List` with your actual project path.

#### Step 2: Make It Executable

bash
chmod +x run_scheduler.sh

#### Step 3: Add to Cron

Open crontab:

bash
crontab -e

Add this line (runs every 15 minutes):

bash
*/15 * * * * /path/to/To-Do-List/run_scheduler.sh

Save and exit.

#### Step 4: Verify Cron is Running

bash
crontab -l

Check logs:

bash
tail -f logs/scheduler.log

---

## 🧪 Testing

Run all tests:

bash
poetry run pytest -v

---

## 🛠️ Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'schedule'`

**Solution:**

bash
poetry add schedule

### Issue: Scheduler not running via Cron

**Check:**

bash
crontab -l
cat logs/scheduler.log

**Common fixes:**
- Ensure `run_scheduler.sh` has correct path  
- Ensure `chmod +x` was applied  
- Check Poetry path with `which poetry`

### Issue: Database connection error

**Check:**

bash
docker ps

If not running:

bash
docker-compose up -d

---

## 📄 License

MIT License.  
Feel free to fork, improve, and contribute!
