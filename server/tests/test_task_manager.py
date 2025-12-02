"""Tests for TaskManager."""

import pytest
from datetime import datetime, timedelta
from todolist_app.models.project import Project
from todolist_app.managers.task_manager import TaskManager
from todolist_app.exceptions.custom_exceptions import (
    TaskNotFoundException,
    MaxLimitException,
    ValidationException,
    InvalidStatusException,
)
from todolist_app.utils.config import Config


class TestTaskManager:
    """Test cases for TaskManager class."""

    @pytest.fixture
    def project(self):
        """Create a test project."""
        return Project(
            id=1, name="Test Project", description="Test project description"
        )

    @pytest.fixture
    def task_manager(self, project):
        """Create a TaskManager with test project."""
        return TaskManager(project)

    @pytest.fixture(autouse=True)
    def reset_ids(self):
        """Reset ID counters before each test."""
        TaskManager.reset_id_counter()
        yield

    def test_create_task_success(self, task_manager):
        """Test successful task creation."""
        task = task_manager.create_task(
            "Task Title Here",
            "This is a detailed task description with enough words for validation",
        )

        assert task.id == 1
        assert task.title == "Task Title Here"
        assert task.status == "todo"
        assert len(task_manager.project.tasks) == 1

    def test_create_task_with_deadline(self, task_manager):
        """Test creating task with deadline."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        task = task_manager.create_task(
            "Task With Deadline",
            "This is a detailed task description with enough words",
            deadline=future_date,
        )

        assert task.deadline is not None

    def test_create_task_invalid_title(self, task_manager):
        """Test task creation with invalid title (exceeds 30 words)."""
        # Create a title with more than 30 words
        long_title = " ".join(["word"] * 31)
        with pytest.raises(ValidationException):
            task_manager.create_task(
                long_title, "This is a detailed task description with enough words"
            )

    def test_create_task_max_limit(self, task_manager, monkeypatch):
        """Test task creation exceeding maximum limit."""
        monkeypatch.setattr(Config, "MAX_NUMBER_OF_TASK", 2)

        task_manager.create_task(
            "First Task", "This is the first task description with enough words"
        )
        task_manager.create_task(
            "Second Task", "This is the second task description with enough words"
        )

        with pytest.raises(MaxLimitException):
            task_manager.create_task(
                "Third Task", "This is the third task description with enough words"
            )

    def test_get_all_tasks(self, task_manager):
        """Test getting all tasks."""
        task_manager.create_task(
            "Task One", "This is the first task description with enough words"
        )
        task_manager.create_task(
            "Task Two", "This is the second task description with enough words"
        )

        tasks = task_manager.get_all_tasks()
        assert len(tasks) == 2

    def test_get_task_by_id_success(self, task_manager):
        """Test getting task by ID successfully."""
        created_task = task_manager.create_task(
            "Test Task", "This is a test task description with enough words"
        )

        retrieved_task = task_manager.get_task_by_id(created_task.id)
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title

    def test_get_task_by_id_not_found(self, task_manager):
        """Test getting task by non-existent ID."""
        with pytest.raises(TaskNotFoundException):
            task_manager.get_task_by_id(999)

    def test_get_tasks_by_status(self, task_manager):
        """Test filtering tasks by status."""
        task_manager.create_task(
            "Todo Task", "This is a todo task description", status="todo"
        )
        task_manager.create_task(
            "Doing Task",
            "This is a doing task description",
            status="doing",  # ✅ Changed from 'in_progress'
        )
        task_manager.create_task(
            "Done Task", "This is a done task description", status="done"
        )

        todo_tasks = task_manager.get_tasks_by_status("todo")
        assert len(todo_tasks) == 1
        assert todo_tasks[0].status == "todo"

        doing_tasks = task_manager.get_tasks_by_status("doing")
        assert len(doing_tasks) == 1
        assert doing_tasks[0].status == "doing"

    def test_update_task_success(self, task_manager):
        """Test successful task update."""
        task = task_manager.create_task(
            "Original Title", "This is the original task description with enough words"
        )

        updated = task_manager.update_task(
            task.id, title="Updated Task Title"
        )

        assert updated.title == "Updated Task Title"

    def test_delete_task_success(self, task_manager):
        """Test successful task deletion."""
        task = task_manager.create_task(
            "Test Task", "This is a test task description with enough words"
        )

        task_manager.delete_task(task.id)
        assert len(task_manager.project.tasks) == 0

    def test_mark_task_as_done(self, task_manager):
        """Test marking task as done."""
        task = task_manager.create_task(
            "Test Task", "This is a test task description with enough words"
        )

        updated_task = task_manager.mark_task_as_done(task.id)
        assert updated_task.status == "done"

    def test_get_pending_tasks(self, task_manager):
        """Test getting pending tasks."""
        task_manager.create_task(
            "Todo Task", "This is a todo task description", status="todo"
        )
        task_manager.create_task(
            "Done Task", "This is a done task description", status="done"
        )

        pending = task_manager.get_pending_tasks()
        assert len(pending) == 1
        assert pending[0].status == "todo"

    def test_get_overdue_tasks(self, task_manager):
        """Test getting overdue tasks."""
        past_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        # Create overdue task (need to bypass validation for testing)
        task1 = task_manager.create_task(
            "Future Task",
            "This is a future task description with enough words",
            deadline=future_date,
        )
        # Manually set past deadline for testing
        task1.deadline = datetime.now() - timedelta(days=7)

        task_manager.create_task(
            "Future Task Two",
            "This is another future task description",
            deadline=future_date,
        )

        overdue = task_manager.get_overdue_tasks()
        assert len(overdue) == 1

    def test_invalid_status(self, task_manager):
        """Test creating task with invalid status."""
        with pytest.raises(InvalidStatusException):
            task_manager.create_task(
                "Test Task",
                "This is a test task description",
                status="invalid_status"
            )

    def test_all_valid_statuses(self, task_manager):
        """Test creating tasks with all valid statuses."""
        # Test all valid statuses: todo, doing, done
        task1 = task_manager.create_task(
            "Todo Task", "Description", status="todo"
        )
        assert task1.status == "todo"

        task2 = task_manager.create_task(
            "Doing Task", "Description", status="doing"
        )
        assert task2.status == "doing"

        task3 = task_manager.create_task(
            "Done Task", "Description", status="done"
        )
        assert task3.status == "done"
