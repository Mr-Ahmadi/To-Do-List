
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

### Example

**Create Project**
```
Enter your choice: 1
Enter project name (1-4 words): My First Project
Enter description (3-20 words): Sample project for testing
✅ Project created successfully! ID: proj_20251016_123456
```

**Create Task**
```
Enter your choice: 6
Enter title (1-5 words): Complete documentation
Enter description (3-30 words): Write documentation for the project
Enter deadline (YYYY-MM-DD): 2025-10-20
✅ Task created successfully! ID: task_20251016_123457
```

**Change Status**
```
Enter your choice: 9
Enter task ID: task_20251016_123457
Enter new status: in_progress
✅ Task status updated successfully!
```

---

## 🧪 Testing

```bash
poetry run pytest                   # Run all tests
poetry run pytest -v                # Verbose output
poetry run pytest --cov=todolist_app tests/    # Coverage report
poetry run pytest --cov-report=html tests/
open htmlcov/index.html             # View HTML report
```

---

## 🛠️ Development

```bash
poetry run black todolist_app/      # Format
poetry run mypy todolist_app/       # Type check
poetry run flake8 todolist_app/     # Lint
```

Run all quality checks:
```bash
poetry run black todolist_app/
poetry run mypy todolist_app/
poetry run flake8 todolist_app/
poetry run pytest --cov=todolist_app tests/
```

---

## 📊 Specifications

| Resource | Default | Env Variable |
|-----------|----------|--------------|
| Projects | 10 | `MAX_NUMBER_OF_PROJECT` |
| Tasks per Project | 50 | `MAX_NUMBER_OF_TASK` |
| Project Name | 1–4 words | `PROJECT_NAME_MIN/MAX_WORDS` |
| Project Description | 3–20 words | `PROJECT_DESCRIPTION_MIN/MAX_WORDS` |
| Task Title | 1–5 words | `TASK_TITLE_MIN/MAX_WORDS` |
| Task Description | 3–30 words | `TASK_DESCRIPTION_MIN/MAX_WORDS` |

---

## 🏗️ Architecture

- **OOP Design** with strict separation: Models, Managers, Validators, CLI  
- **Single Responsibility Principle** on class level  
- **Configuration** via `.env`  
- **Custom Exceptions** for robust error handling

---

## 🔒 Error Handling

| Exception | Description |
|------------|--------------|
| `ValidationException` | Invalid data |
| `ProjectNotFoundException` | Project missing |
| `TaskNotFoundException` | Task missing |
| `DuplicateProjectException` | Duplicate project name |
| `MaxLimitException` | Exceeded limits |
| `InvalidStatusException` | Invalid task status |
| `InvalidDateException` | Past/invalid date |

---

## 📝 Git Workflow

**Branches**
- `main`: stable release  
- `develop`: integration branch  
- `feature/*`: feature branches  

**Commit Convention**
```
feat: add new feature
fix: resolve a bug
docs: update docs
style: code format
refactor: improve code structure
test: add/update tests
chore: update build/deps
```

---

## 🤝 Contributing

1. Fork repository  
2. Create branch: `git checkout -b feature/awesome-feature`  
3. Implement & test changes  
4. Format & lint  
5. Commit and push  
6. Open pull request  

---

## 🗺️ Roadmap

**Phase 1 (✅ Completed)**  
- In-memory storage, validation, CLI  

**Phase 2 (Planned)**  
- Persistence (JSON/CSV), Task tags, Priority  

**Phase 3 (Future)**  
- Database (SQLite/Postgres), Web UI, Auth, Notifications  

---

## 📄 License

Licensed under [MIT](LICENSE) © 2025 **Ali Ahmadi**

---

## 👨‍💻 Author

**Ali Ahmadi**  
GitHub: [@yourusername](https://github.com/yourusername)  
Email: your.email@example.com  

---

## 🙏 Acknowledgments
Inspired by modern task tools, built with Python OOP best practices, using:
- **Poetry** for dependency management  
- **pytest**, **black**, **mypy** for quality assurance  

---

## 📞 Support

- See [Troubleshooting](#🧪-testing) / `docs/` folder  
- Open an issue: [GitHub Issues](https://github.com/yourusername/To-Do-List/issues)  
- Contact: your.email@example.com  

---

<div align="center">

**Made with ❤️ using Python and Poetry**  
[Report Bug](https://github.com/yourusername/To-Do-List/issues) · 
[Request Feature](https://github.com/yourusername/To-Do-List/issues)

</div>

---

## ⚙️ CI/CD (.github/workflows/ci.yml)

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11, 3.12]

    steps:
      - uses: actions/checkout@v3
      - name: Install Poetry
        run: pipx install poetry
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'poetry'
      - name: Install dependencies
        run: poetry install
      - name: Run tests with coverage
        run: poetry run pytest --cov=todolist_app tests/
      - name: Black format check
        run: poetry run black --check todolist_app/
      - name: Lint check
        run: poetry run flake8 todolist_app/
      - name: Mypy type check
        run: poetry run mypy todolist_app/
