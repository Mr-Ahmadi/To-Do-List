"""Tests for Validators."""

import pytest
from datetime import datetime, timedelta
from todolist_app.utils.validators import Validator
from todolist_app.exceptions.custom_exceptions import (
    ValidationException,
    InvalidStatusException,
    InvalidDateException,
)


class TestValidators:
    """Test cases for Validator class."""

    def test_validate_word_count_valid(self):
        """Test word count validation with valid input."""
        # Should not raise exception
        Validator.validate_word_count("Hello World", 2, 3, "Test Field")

    def test_validate_word_count_too_few(self):
        """Test word count validation with too few words."""
        with pytest.raises(ValidationException) as exc_info:
            Validator.validate_word_count("Hello", 2, 3, "Test Field")
        assert "at least 2 words" in str(exc_info.value)

    def test_validate_word_count_too_many(self):
        """Test word count validation with too many words."""
        with pytest.raises(ValidationException) as exc_info:
            Validator.validate_word_count(
                "One Two Three Four", 2, 3, "Test Field"
            )
        assert "not exceed 3 words" in str(exc_info.value)

    def test_validate_word_count_empty(self):
        """Test word count validation with empty string."""
        with pytest.raises(ValidationException) as exc_info:
            Validator.validate_word_count("", 2, 3, "Test Field")
        assert "cannot be empty" in str(exc_info.value)

    def test_validate_status_valid(self):
        """Test status validation with valid status."""
        # Should not raise exception
        Validator.validate_status("todo")
        Validator.validate_status("in_progress")
        Validator.validate_status("done")

    def test_validate_status_invalid(self):
        """Test status validation with invalid status."""
        with pytest.raises(InvalidStatusException) as exc_info:
            Validator.validate_status("invalid_status")
        assert "Invalid status" in str(exc_info.value)

    def test_validate_deadline_valid(self):
        """Test deadline validation with valid future date."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        result = Validator.validate_deadline(future_date)
        assert isinstance(result, datetime)

    def test_validate_deadline_invalid_format(self):
        """Test deadline validation with invalid format."""
        with pytest.raises(InvalidDateException) as exc_info:
            Validator.validate_deadline("2025/12/31")
        assert "Invalid date format" in str(exc_info.value)

    def test_validate_deadline_past_date(self):
        """Test deadline validation with past date."""
        past_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        with pytest.raises(InvalidDateException) as exc_info:
            Validator.validate_deadline(past_date)
        assert "cannot be in the past" in str(exc_info.value)

    def test_validate_deadline_none(self):
        """Test deadline validation with None."""
        result = Validator.validate_deadline(None)
        assert result is None

    def test_validate_deadline_empty(self):
        """Test deadline validation with empty string."""
        result = Validator.validate_deadline("")
        assert result is None

    def test_validate_positive_integer_valid(self):
        """Test positive integer validation with valid input."""
        result = Validator.validate_positive_integer("5", "Test Field")
        assert result == 5

    def test_validate_positive_integer_zero(self):
        """Test positive integer validation with zero."""
        with pytest.raises(ValidationException) as exc_info:
            Validator.validate_positive_integer("0", "Test Field")
        assert "positive integer" in str(exc_info.value)

    def test_validate_positive_integer_negative(self):
        """Test positive integer validation with negative number."""
        with pytest.raises(ValidationException) as exc_info:
            Validator.validate_positive_integer("-5", "Test Field")
        assert "positive integer" in str(exc_info.value)

    def test_validate_positive_integer_invalid(self):
        """Test positive integer validation with non-integer."""
        with pytest.raises(ValidationException) as exc_info:
            Validator.validate_positive_integer("abc", "Test Field")
        assert "valid integer" in str(exc_info.value)
