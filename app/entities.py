from datetime import datetime
from .exceptions import InvalidDateFormatError, FutureDateError


class Field:
    """Base class for record fields."""
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Address(Field):
    """Class for storing contact address."""
    
    def __init__(self, value):
        # Check that address is not empty
        if not value or not value.strip():
            raise ValueError("Address cannot be empty")
        
        # Remove leading and trailing whitespace
        super().__init__(value.strip())


class Birthday(Field):
    """Class for storing birthday with validation."""
    
    def __init__(self, value):
        try:
            # Parse string into datetime object
            # Format: DD.MM.YYYY (e.g., 25.12.1990)
            birthday = datetime.strptime(value, "%d.%m.%Y")
            
            # Check that date is not in the future
            if birthday > datetime.now():
                raise FutureDateError("Birthday cannot be in the future")
            
            # Store as datetime object (not string!)
            super().__init__(birthday)
            
        except ValueError:
            # If strptime failed to parse
            raise InvalidDateFormatError(
                f"Invalid date format: {value}. "
                "Expected format: DD.MM.YYYY (e.g., 25.12.1990)"
            )