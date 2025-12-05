Below is a **cleaned, professional, and concise README** that preserves **all your original content**, but with better structure, consistency, spacing, and readability.

---

# **To-Do List Project – Phase 3 (Web API)**

![Phase 3](https://img.shields.io/badge/Phase-3%20Web%20API-100%25%20Complete-success)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat\&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791?logo=postgresql)

**Software Engineering Course – AUT – December 2025**

---

## 🚨 CLI Deprecation Notice

> **The old CLI (Phases 1 & 2) is officially deprecated as of Phase 3.**
> It still works for backward compatibility, but will be removed in a future version.
> **All new development and usage must use the Web API.**

**Web API Documentation:**

* Swagger UI → [http://localhost:8002/docs](http://localhost:8002/docs)
* ReDoc → [http://localhost:8002/redoc](http://localhost:8002/redoc)

---

## 📈 Project Evolution

| Phase | Year     | Storage                 | Architecture                     | Interface                     | Status      |
| ----- | -------- | ----------------------- | -------------------------------- | ----------------------------- | ----------- |
| 1     | 2024     | In-Memory               | OOP + Basic Structure            | CLI                           | ✓ Completed |
| 2     | 2025     | PostgreSQL + SQLAlchemy | Layered + Repository + Scheduler | CLI                           | ✓ Completed |
| **3** | **2025** | **PostgreSQL**          | **Layered + Presentation Layer** | **RESTful Web API (FastAPI)** | ⭐ Current   |

**Phase 3 introduces a full production-grade Web API** while keeping all domain logic from previous phases.

---

## 🌐 Phase 3 Web API Features

* RESTful API with clean resource naming
* Built with **FastAPI** (auto OpenAPI docs)
* Input validation with **Pydantic**
* Projects + Tasks with hierarchical structure
* Task filtering by status
* Overdue detection + automatic deadline-based updates
* Accurate HTTP status codes (201, 204, …)
* Relationship eager loading
* Scheduler for automatic overdue task closure
* Frontend-ready (React, Vue, etc.)
* Clear layered architecture:
  **API → Service → Manager → Repository → Model → Database**

---

## 📘 API Documentation (Auto-generated)

* **Swagger UI:** [http://localhost:8002/docs](http://localhost:8002/docs)
* **ReDoc:** [http://localhost:8002/redoc](http://localhost:8002/redoc)

---

## 📂 Main Endpoints

### **Projects**

| Method | Endpoint             | Description       |
| ------ | -------------------- | ----------------- |
| GET    | `/api/projects/`     | List all projects |
| POST   | `/api/projects/`     | Create a project  |
| GET    | `/api/projects/{id}` | Get project       |
| PUT    | `/api/projects/{id}` | Update project    |
| DELETE | `/api/projects/{id}` | Delete project    |

### **Tasks**

| Method | Endpoint                    | Description             |
| ------ | --------------------------- | ----------------------- |
| GET    | `/api/tasks/?project_id=1`  | List tasks in a project |
| GET    | `/api/tasks/?status=todo`   | Filter tasks by status  |
| GET    | `/api/tasks/overdue`        | Get overdue tasks       |
| POST   | `/api/tasks/`               | Create task             |
| GET    | `/api/tasks/{id}`           | Get task                |
| PUT    | `/api/tasks/{id}`           | Update task             |
| PATCH  | `/api/tasks/{id}/mark-done` | Mark as done            |
| DELETE | `/api/tasks/{id}`           | Delete task             |

---

## ▶️ How to Run (Phase 3 – Recommended)

```bash
# Install dependencies
poetry install

# Ensure PostgreSQL is running and DATABASE_URL is set

# Start the Web API
poetry run uvicorn todolist_app.api.main:app --reload --host 0.0.0.0 --port 8002
```

Open → [http://localhost:8002/docs](http://localhost:8002/docs)

### Production Port

```bash
poetry run uvicorn todolist_app.api.main:app --host 0.0.0.0 --port $PORT
```

---

## ⏱ Scheduler (Auto-close overdue tasks)

```bash
./run_scheduler.sh
```

Or manually:

```bash
poetry run python -m todolist_app.scheduler.autoclose_runner >> scheduler.log 2>&1
```

---

## ⚠️ Running the Deprecated CLI

```bash
poetry run todolist
```

Displays:

```
WARNING: CLI interface is officially DEPRECATED (Phase 3).
Please use the Web API at http://localhost:8002/docs
```

---

## 📁 Project Structure (Phase 3)

```
todolist_app/
├── api/
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   └── schemas/
├── models/
├── repositories/
├── services/
├── db/
├── cli/                # Deprecated
├── scheduler/
├── exceptions/
├── utils/
└── alembic/            # DB migrations
```

---

## 🛠 Technology Stack

* **FastAPI**
* **SQLAlchemy 2.0+**
* **PostgreSQL**
* **Pydantic**
* **Poetry**
* **Uvicorn**
* **Alembic**

---

## 📮 API Usage Examples (HTTP Client)

```http
### BASE CONFIG
@base_url = http://localhost:8002/api
@contentType = application/json

### Create a project
POST {{base_url}}/projects/
Content-Type: {{contentType}}

{
  "name": "Website Redesign",
  "description": "Full redesign project"
}

### Create a task
POST {{base_url}}/tasks/
Content-Type: {{contentType}}

{
  "title": "Design UI",
  "description": "Create UI/UX wireframes",
  "project_id": 1,
  "deadline": "2025-12-10",
  "status": "todo"
}

### List tasks in project
GET {{base_url}}/tasks/?project_id=1

### Filter by status
GET {{base_url}}/tasks/?project_id=1&status=doing

### Overdue tasks
GET {{base_url}}/tasks/overdue

### Mark as done
PATCH {{base_url}}/tasks/1/mark-done
```

---


## ⚙️ Scripts

* `run_server.sh` – Start server
* `run_scheduler.sh` – Run overdue scheduler

---

## 🌱 Environment Setup

Set your DB URL:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/todolist"
```

Or set it in `todolist_app/utils/config.py`.

---

## 📌 Notes

* All endpoints are prefixed with `/api`
* Tasks require a valid `project_id`
* Valid task statuses: `todo`, `doing`, `done`
* Deadline format: **YYYY-MM-DD**
* Scheduler auto-updates overdue tasks
