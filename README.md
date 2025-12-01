# 📋 ToDoList Application

A **CLI-based task management system** built with
**Python OOP**, **SQLAlchemy ORM**, **PostgreSQL**, **Docker**, and **Alembic**.

The application now uses a **fully persistent PostgreSQL database**, replacing the previous in-memory storage model.

**NEW:** Automated overdue-task closure through **scheduled commands** (Cron or Python scheduler).

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

### Scheduled Task Automation ✨ **NEW**

- **Automatic closure of overdue tasks**  
- Command: `tasks:autoclose-overdue` (sets `status=done`, `closed_at=now`)  
- Can be triggered:
  - Manually via CLI  
  - Automatically via Python scheduler (`schedule` library)  
  - Automatically via Cron Job (runs every 15 minutes)

### Data Validation
