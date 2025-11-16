"""Custom exceptions for the application."""


class InvalidDateFormatError(Exception):
    """Exception raised when date format is invalid."""

    pass


class FutureDateError(Exception):
    """Exception raised when date is in the future."""

    pass
