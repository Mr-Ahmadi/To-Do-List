import pytest
from datetime import datetime
from todolist_app.utils.validators import Validator
from todolist_app.exceptions.custom_exceptions import (
    ValidationException,
    InvalidStatusException,
    InvalidDateException,
)


class TestValidator:
    """Test suite for Validator class."""

    # ============= Project Name Tests =============
    def test_validate_project_name_valid_single_word(self):
        """Test validation passes for single word name."""
        Validator.validate_project_name("MyProject")  # Should not raise

    def test_validate_project_name_valid_multiple_words(self):
        """Test validation passes for multiple words."""
        Validator.validate_project_name("My Awesome Project")  # Should not raise

    def test_validate_project_name_empty(self):
        """Test validation fails for empty name."""
        with pytest.raises(ValidationException, match="cannot be empty"):
            Validator.validate_project_name("")

    def test_validate_project_name_whitespace_only(self):
        """Test validation fails for whitespace only."""
        with pytest.raises(ValidationException, match="cannot be empty"):
            Validator.validate_project_name("   ")

    def test_validate_project_name_exceeds_max_words(self):
        """Test validation fails when exceeding max word count."""
        long_name = " ".join(["word"] * 31)  # 31 words
        with pytest.raises(ValidationException, match="cannot exceed 30 words"):
            Validator.validate_project_name(long_name)

    # ============= Project Description Tests =============
    def test_validate_project_description_empty(self):
        """Test validation passes for empty description."""
        Validator.validate_project_description("")  # Should not raise

    def test_validate_project_description_none(self):
        """Test validation passes for None description."""
        Validator.validate_project_description(None)  # Should not raise

    def test_validate_project_description_valid(self):
        """Test validation passes for valid description."""
        desc = "This is a valid project description with multiple words."
        Validator.validate_project_description(desc)  # Should not raise

    def test_validate_project_description_exceeds_max_words(self):
        """Test validation fails when exceeding max word count."""
        long_desc = " ".join(["word"] * 151)  # 151 words
        with pytest.raises(ValidationException, match="cannot exceed 150 words"):
            Validator.validate_project_description(long_desc)

    # ============= Task Title Tests =============
    def test_validate_task_title_valid_single_word(self):
        """Test validation passes for single word title."""
        Validator.validate_task_title("Task")  # Should not raise

    def test_validate_task_title_valid_multiple_words(self):
        """Test validation passes for multiple words."""
        Validator.validate_task_title("Implement Feature X")  # Should not raise

    def test_validate_task_title_empty(self):
        """Test validation fails for empty title."""
        with pytest.raises(ValidationException, match="cannot be empty"):
            Validator.validate_task_title("")

    def test_validate_task_title_exceeds_max_words(self):
        """Test validation fails when exceeding max word count."""
        long_title = " ".join(["word"] * 31)  # 31 words
        with pytest.raises(ValidationException, match="cannot exceed 30 words"):
            Validator.validate_task_title(long_title)

    # ============= Task Description Tests =============
    def test_validate_task_description_valid(self):
        """Test validation passes for valid description."""
        desc = "This is a valid task description."
        Validator.validate_task_description(desc)  # Should not raise

    def test_validate_task_description_empty(self):
        """Test validation fails for empty description."""
        with pytest.raises(ValidationException, match="cannot be empty"):
            Validator.validate_task_description("")

    def test_validate_task_description_exceeds_max_words(self):
        """Test validation fails when exceeding max word count."""
        long_desc = " ".join(["word"] * 151)  # 151 words
        with pytest.raises(ValidationException, match="cannot exceed 150 words"):
            Validator.validate_task_description(long_desc)

    # ============= Status Tests =============
    def test_validate_status_valid_todo(self):
        """Test validation passes for 'todo' status."""
        Validator.validate_status("todo")  # Should not raise

    def test_validate_status_valid_doing(self):
        """Test validation passes for 'doing' status."""
        Validator.validate_status("doing")  # Should not raise

    def test_validate_status_valid_done(self):
        """Test validation passes for 'done' status."""
        Validator.validate_status("done")  # Should not raise

    def test_validate_status_invalid(self):
        """Test validation fails for invalid status."""
        with pytest.raises(InvalidStatusException, match="Invalid status"):
            Validator.validate_status("pending")

    # ============= Deadline Tests =============
    def test_validate_deadline_valid(self):
        """Test validation passes for valid date."""
        result = Validator.validate_deadline("2024-12-31")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 12
        assert result.day == 31

    def test_validate_deadline_none(self):
        """Test validation passes for None."""
        result = Validator.validate_deadline(None)
        assert result is None

    def test_validate_deadline_empty_string(self):
        """Test validation passes for empty string."""
        result = Validator.validate_deadline("")
        assert result is None

    def test_validate_deadline_invalid_format(self):
        """Test validation fails for invalid date format."""
        with pytest.raises(InvalidDateException, match="Invalid date format"):
            Validator.validate_deadline("31-12-2024")

    def test_validate_deadline_invalid_date(self):
        """Test validation fails for invalid date."""
        with pytest.raises(InvalidDateException, match="Invalid date format"):
            Validator.validate_deadline("2024-13-01")  # Invalid month

    # ============= ID Tests =============
    def test_validate_id_valid(self):
        """Test validation passes for valid ID."""
        Validator.validate_id(1, "project")  # Should not raise

    def test_validate_id_zero(self):
        """Test validation fails for zero ID."""
        with pytest.raises(ValidationException, match="must be a positive integer"):
            Validator.validate_id(0, "project")

    def test_validate_id_negative(self):
        """Test validation fails for negative ID."""
        with pytest.raises(ValidationException, match="must be a positive integer"):
            Validator.validate_id(-1, "project")

    def test_validate_id_non_integer(self):
        """Test validation fails for non-integer ID."""
        with pytest.raises(ValidationException, match="must be an integer"):
            Validator.validate_id("1", "project")