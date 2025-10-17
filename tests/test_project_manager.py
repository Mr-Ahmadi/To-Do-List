"""Tests for ProjectManager."""

import pytest
from todolist_app.managers.project_manager import ProjectManager
from todolist_app.exceptions.custom_exceptions import (
    ProjectNotFoundException,
    DuplicateProjectException,
    MaxLimitException,
    ValidationException,
)
from todolist_app.utils.config import Config


class TestProjectManager:
    """Test cases for ProjectManager class."""

    def test_create_project_success(self):
        """Test successful project creation."""
        manager = ProjectManager()
        project = manager.create_project(
            "Test Project Name", "This is a test project description with enough words"
        )

        assert project.id == 1
        assert project.name == "Test Project Name"
        assert len(manager.projects) == 1

    def test_create_project_invalid_name(self):
        """Test project creation with invalid name."""
        manager = ProjectManager()
        with pytest.raises(ValidationException):
            manager.create_project(
                "Short", "This is a test project description with enough words"
            )

    def test_create_project_duplicate_name(self):
        """Test creating project with duplicate name."""
        manager = ProjectManager()
        manager.create_project(
            "Test Project Name", "This is a test project description with enough words"
        )

        with pytest.raises(DuplicateProjectException):
            manager.create_project(
                "Test Project Name",
                "Another test project description with enough words",
            )

    def test_create_project_max_limit(self, monkeypatch):
        """Test project creation exceeding maximum limit."""
        # Temporarily set max projects to 2 for testing
        monkeypatch.setattr(Config, "MAX_NUMBER_OF_PROJECT", 2)

        manager = ProjectManager()
        manager.create_project(
            "First Project", "This is the first test project with enough words"
        )
        manager.create_project(
            "Second Project", "This is the second test project with enough words"
        )

        with pytest.raises(MaxLimitException):
            manager.create_project(
                "Third Project", "This is the third test project with enough words"
            )

    def test_get_all_projects(self):
        """Test getting all projects."""
        manager = ProjectManager()
        manager.create_project(
            "Project One", "This is the first test project with enough words"
        )
        manager.create_project(
            "Project Two", "This is the second test project with enough words"
        )

        projects = manager.get_all_projects()
        assert len(projects) == 2

    def test_get_project_by_id_success(self):
        """Test getting project by ID successfully."""
        manager = ProjectManager()
        created_project = manager.create_project(
            "Test Project", "This is a test project description with enough words"
        )

        retrieved_project = manager.get_project_by_id(created_project.id)
        assert retrieved_project.id == created_project.id
        assert retrieved_project.name == created_project.name

    def test_get_project_by_id_not_found(self):
        """Test getting project by non-existent ID."""
        manager = ProjectManager()
        with pytest.raises(ProjectNotFoundException):
            manager.get_project_by_id(999)

    def test_update_project_success(self):
        """Test successful project update."""
        manager = ProjectManager()
        project = manager.create_project(
            "Original Name", "This is the original description with enough words"
        )

        updated = manager.update_project(
            project.id, "Updated Project Name", "This is the updated description text"
        )

        assert updated.name == "Updated Project Name"
        assert updated.description == "This is the updated description text"

    def test_delete_project_success(self):
        """Test successful project deletion."""
        manager = ProjectManager()
        project = manager.create_project(
            "Test Project", "This is a test project description with enough words"
        )

        manager.delete_project(project.id)
        assert len(manager.projects) == 0

    def test_delete_project_not_found(self):
        """Test deleting non-existent project."""
        manager = ProjectManager()
        with pytest.raises(ProjectNotFoundException):
            manager.delete_project(999)

    def test_search_projects(self):
        """Test searching projects."""
        manager = ProjectManager()
        manager.create_project(
            "Python Project", "A project about Python programming with tests"
        )
        manager.create_project(
            "Java Project", "A project about Java programming language today"
        )

        results = manager.search_projects("Python")
        assert len(results) == 1
        assert results[0].name == "Python Project"
