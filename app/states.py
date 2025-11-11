import re


class Phone(Field):
    """Class Phone with normalize and validation func."""
    
    def __init__(self, value):
        cleaned_phone = self._clean_and_normalize_phone(value)
        self._validate_phone(cleaned_phone)
        super().__init__(cleaned_phone)
    
    def _clean_and_normalize_phone(self, phone_number):
        """Clean and normalize phone number."""
        # Remove leading/trailing whitespace
        phone_number = phone_number.strip()

        # Remove all non-digit characters
        phone_number = re.sub(r"[^\d]", "", phone_number)

        # Handle different formats
        if phone_number.startswith("380") and len(phone_number) > 10:
            # Full Ukrainian number with country code
            return phone_number[2:]
        else:
            # Other cases
            return phone_number
    
    def _validate_phone(self, phone):
        """Validate cleaned phone number."""
        # Check length - exactly 10 digits
        if len(phone) != 10:
            raise ValueError(
                f"Phone number must contain exactly 10 digits. "
                f"Got {len(phone)} digits: '{phone}'"
            )

