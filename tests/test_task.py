"""Tests for Task model."""

import pytest
from datetime import datetime, timedelta
from todolist_app.models.task import Task


class TestTask:
    """Test cases for Task class."""

    def test_task_creation_without_deadline(self):
        """Test creating a task without deadline."""
        task = Task(
            id=1, title="Test Task", description="Test Description", project_id=1
        )

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.project_id == 1
        assert task.deadline is None
        assert task.status == "todo"
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_creation_with_deadline(self):
        """Test creating a task with deadline."""
        deadline = datetime.now() + timedelta(days=7)
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            project_id=1,
            deadline=deadline,
        )

        assert task.deadline == deadline

    def test_task_creation_with_status(self):
        """Test creating a task with custom status."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            project_id=1,
            status="in_progress",
        )

        assert task.status == "in_progress"

    def test_task_update(self):
        """Test updating task details."""
        task = Task(
            id=1, title="Old Title", description="Old Description", project_id=1
        )
        old_updated_at = task.updated_at

        import time
        time.sleep(0.01)

        new_deadline = datetime.now() + timedelta(days=5)
        task.update(
            title="New Title",
            description="New Description",
            deadline=new_deadline,
            status="in_progress",
        )

        assert task.title == "New Title"
        assert task.description == "New Description"
        assert task.deadline == new_deadline
        assert task.status == "in_progress"
        assert task.updated_at > old_updated_at

    def test_task_partial_update(self):
        """Test updating only some fields."""
        task = Task(
            id=1, title="Test Title", description="Test Description", project_id=1
        )

        task.update(status="done")

        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.status == "done"

    def test_task_str_representation(self):
        """Test string representation of task."""
        task = Task(
            id=1, title="Test Task", description="Test Description", project_id=1
        )

        str_repr = str(task)

        assert "Test Task" in str_repr
        assert "Test Description" in str_repr
        assert "Task ID: 1" in str_repr
        assert "todo" in str_repr

    def test_task_repr(self):
        """Test repr representation of task."""
        task = Task(
            id=1, title="Test Task", description="Test Description", project_id=1
        )

        repr_str = repr(task)

        assert "Task" in repr_str
        assert "id=1" in repr_str
        assert "title='Test Task'" in repr_str
        assert "status='todo'" in repr_str
