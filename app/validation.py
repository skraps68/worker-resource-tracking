"""Validation utilities for worker resource tracking system."""
from datetime import datetime, date
from typing import Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_date_range(start_date, end_date, start_field_name="start", end_field_name="end"):
    """
    Validate that start date is less than or equal to end date.
    
    Args:
        start_date: Start date (date or datetime)
        end_date: End date (date or datetime)
        start_field_name: Name of start field for error messages
        end_field_name: Name of end field for error messages
        
    Raises:
        ValidationError: If start_date > end_date
    """
    if start_date is None or end_date is None:
        return
    
    if start_date > end_date:
        raise ValidationError(
            f"{start_field_name} must be less than or equal to {end_field_name}"
        )


def validate_processing_time_range(proc_start: datetime, proc_end: datetime):
    """
    Validate that processing start is less than or equal to processing end.
    
    Args:
        proc_start: Processing start datetime
        proc_end: Processing end datetime
        
    Raises:
        ValidationError: If proc_start > proc_end
    """
    validate_date_range(proc_start, proc_end, "proc_start", "proc_end")


def validate_business_time_range(res_start: date, res_end: date):
    """
    Validate that resource start is less than or equal to resource end.
    
    Args:
        res_start: Resource start date
        res_end: Resource end date
        
    Raises:
        ValidationError: If res_start > res_end
    """
    validate_date_range(res_start, res_end, "res_start", "res_end")


def validate_required_field(value, field_name: str):
    """
    Validate that a required field is not None or empty.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error messages
        
    Raises:
        ValidationError: If value is None or empty string
    """
    if value is None:
        raise ValidationError(f"Required field '{field_name}' is missing")
    
    if isinstance(value, str) and not value.strip():
        raise ValidationError(f"Required field '{field_name}' cannot be empty")


def validate_date_format(value, field_name: str) -> date:
    """
    Validate and parse a date value.
    
    Args:
        value: The value to validate (can be date, str, or None)
        field_name: Name of the field for error messages
        
    Returns:
        Parsed date object
        
    Raises:
        ValidationError: If value is not a valid date
    """
    if value is None:
        raise ValidationError(f"Required field '{field_name}' is missing")
    
    if isinstance(value, date):
        return value
    
    if isinstance(value, str):
        try:
            # Try parsing YYYY-MM-DD format
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(f"Invalid date format for '{field_name}'. Expected YYYY-MM-DD")
    
    raise ValidationError(f"Invalid date format for '{field_name}'")


def validate_datetime_format(value, field_name: str) -> datetime:
    """
    Validate and parse a datetime value.
    
    Args:
        value: The value to validate (can be datetime, str, or None)
        field_name: Name of the field for error messages
        
    Returns:
        Parsed datetime object
        
    Raises:
        ValidationError: If value is not a valid datetime
    """
    if value is None:
        raise ValidationError(f"Required field '{field_name}' is missing")
    
    if isinstance(value, datetime):
        return value
    
    if isinstance(value, str):
        try:
            # Try parsing YYYY-MM-DD HH:MM:SS format
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValidationError(
                f"Invalid datetime format for '{field_name}'. Expected YYYY-MM-DD HH:MM:SS"
            )
    
    raise ValidationError(f"Invalid datetime format for '{field_name}'")
