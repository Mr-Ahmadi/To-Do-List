"""Tests for Project model."""

import pytest
from datetime import datetime
from todolist_app.models.project import Project
from todolist_app.models.task import Task


class TestProject:
    """Test cases for Project class."""

    def test_project_creation(self):
        """Test creating a new project."""
        project = Project(id=1, name="Test Project", description="Test Description")

        assert project.id == 1
        assert project.name == "Test Project"
        assert project.description == "Test Description"
        assert isinstance(project.created_at, datetime)
        assert isinstance(project.updated_at, datetime)
        assert project.tasks == []

    def test_project_update(self):
        """Test updating project details."""
        project = Project(id=1, name="Old Name", description="Old Description")
        old_updated_at = project.updated_at

        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)

        project.update(name="New Name", description="New Description")

        assert project.name == "New Name"
        assert project.description == "New Description"
        assert project.updated_at > old_updated_at

    def test_project_partial_update(self):
        """Test updating only some fields."""
        project = Project(id=1, name="Test Name", description="Test Description")

        project.update(name="Updated Name")

        assert project.name == "Updated Name"
        assert project.description == "Test Description"

    def test_project_add_task(self):
        """Test adding tasks to project."""
        project = Project(id=1, name="Test Project", description="Test Description")
        task = Task(
            id=1, title="Test Task", description="Task Description", project_id=1
        )

        project.tasks.append(task)

        assert len(project.tasks) == 1
        assert project.tasks[0].title == "Test Task"

    def test_project_str_representation(self):
        """Test string representation of project."""
        project = Project(id=1, name="Test Project", description="Test Description")

        str_repr = str(project)

        assert "Test Project" in str_repr
        assert "Test Description" in str_repr
        assert "Project ID: 1" in str_repr

    def test_project_repr(self):
        """Test repr representation of project."""
        project = Project(id=1, name="Test Project", description="Test Description")

        repr_str = repr(project)

        assert "Project" in repr_str
        assert "id=1" in repr_str
        assert "name='Test Project'" in repr_str
