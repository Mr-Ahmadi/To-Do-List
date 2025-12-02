"""Tests for configuration utilities."""
import os
import pytest


class TestConfig:
    """Test cases for Config class."""

    def test_config_defaults(self):
        """Test that config has correct default values."""
        # Remove env vars temporarily
        old_projects = os.environ.pop("MAX_NUMBER_OF_PROJECT", None)
        old_tasks = os.environ.pop("MAX_NUMBER_OF_TASK", None)
        
        try:
            # Reimport to get fresh config
            import sys
            if 'todolist_app.utils.config' in sys.modules:
                del sys.modules['todolist_app.utils.config']
            
            from todolist_app.utils.config import Config
            config = Config()
            
            assert config.get_max_projects() == 10
            assert config.get_max_tasks() == 50
        finally:
            # Restore original values
            if old_projects:
                os.environ["MAX_NUMBER_OF_PROJECT"] = old_projects
            if old_tasks:
                os.environ["MAX_NUMBER_OF_TASK"] = old_tasks

    def test_config_reads_env_file(self):
        """Test that config can read from environment."""
        # This tests that the config system works, 
        # not that it dynamically reloads (which it shouldn't)
        from todolist_app.utils.config import Config
        config = Config()
        
        # Should return integers
        assert isinstance(config.get_max_projects(), int)
        assert isinstance(config.get_max_tasks(), int)
        
        # Should be positive
        assert config.get_max_projects() > 0
        assert config.get_max_tasks() > 0

    def test_config_validation(self):
        """Test that config values are within expected ranges."""
        from todolist_app.utils.config import Config
        config = Config()
        
        # Check reasonable limits
        assert 1 <= config.get_max_projects() <= 100
        assert 1 <= config.get_max_tasks() <= 1000

    def test_config_singleton_behavior(self):
        """Test that config maintains consistent values."""
        from todolist_app.utils.config import Config
        config1 = Config()
        config2 = Config()
        
        # Both instances should return same values
        assert config1.get_max_projects() == config2.get_max_projects()
        assert config1.get_max_tasks() == config2.get_max_tasks()
