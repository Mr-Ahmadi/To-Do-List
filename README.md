
---

# 📋 ToDoList Application

A **CLI-based task management system** built with **Python OOP principles**, featuring project and task handling with in-memory storage.

[![Python Version](https://img.shields.io/badge/python-3.8.1%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/dependency%20management-poetry-blue)](https://python-poetry.org/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 Features

### Project Management
- Create, read, update, delete projects  
- Configurable limit (default: **10 projects**)  
- Word count validation for names/descriptions  
- Duplicate name prevention  
- View all active projects with details  

### Task Management
- CRUD operations within projects  
- Up to **50 tasks per project** (configurable)  
- Statuses: `todo`, `in_progress`, `done`  
- Optional validated deadlines (future `YYYY-MM-DD`)  
- Search tasks by title/description  
- View overdue tasks  
- Project completion tracking  

### Data Validation
- Word count and format checks  
- Status whitelist validation  
- Date format and future date verification  
- Comprehensive custom exceptions  

---

## 📁 Project Structure

```bash
To-Do-List/
├── todolist_app/
│   ├── cli/
│   │   └── main.py
│   ├── models/            # Project, Task
│   ├── managers/          # ProjectManager, TaskManager
│   ├── utils/             # Config + Validators
│   └── exceptions/
├── tests/
│   ├── test_project.py
│   ├── test_task.py
│   ├── test_validators.py
│   ├── test_project_manager.py
│   └── test_task_manager.py
├── docs/
├── main.py
├── pyproject.toml
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- **Python ≥ 3.8.1**
- **Poetry** installed

### Install Poetry
```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Verify installation:
```bash
poetry --version
```

---

### Installation
```bash
git clone https://github.com/yourusername/To-Do-List.git
cd To-Do-List
poetry install
```

Create a `.env` file in project root:
```bash
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50
PROJECT_NAME_MIN_WORDS=1
PROJECT_NAME_MAX_WORDS=4
PROJECT_DESCRIPTION_MIN_WORDS=3
PROJECT_DESCRIPTION_MAX_WORDS=20
TASK_TITLE_MIN_WORDS=1
TASK_TITLE_MAX_WORDS=5
TASK_DESCRIPTION_MIN_WORDS=3
TASK_DESCRIPTION_MAX_WORDS=30
```

---

## 🎯 Usage

### Run the Application
```bash
poetry run todolist
# or
poetry shell
todolist
```

### Main Menu
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
