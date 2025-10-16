"""Tests for CLI interface."""
import pytest
from unittest.mock import patch, MagicMock
from todolist_app.cli.main import TodoListCLI


class TestCLI:
    """Test CLI interface."""
    
    @patch('builtins.input', side_effect=['1', 'Test Project', 'Test description here', '0'])
    @patch('builtins.print')
    def test_create_project_via_cli(self, mock_print, mock_input):
        """Test creating project through CLI."""
        cli = TodoListCLI()
        # CLI test implementation
        pass
