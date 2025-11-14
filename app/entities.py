from typing import List, Optional


class Field:
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

class Record:
    """
    Represents a single contact in the address book.

    Uses composition of field classes:
    - Name (required)
    - Phone (multiple)
    - Email (multiple)
    - Address (multiple)
    - Birthday (optional)
    """

    def __init__(self, name: str) -> None:
        """
        Create a new contact record.

        :param name: Contact name as a string.
        """
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.emails: List[Email] = []
        self.addresses: List[Address] = []
        self.birthday: Optional[Birthday] = None

    # ---------- phone methods ----------

    def add_phone(self, phone: str) -> None:
        """
        Add a new phone number to the contact.

        Validation is handled inside the Phone class.

        :param phone: Phone number as a string.
        """
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> Optional[Phone]:
        """
        Find a phone object by its numeric value.

        :param phone: Phone number to search for.
        :return: Phone instance if found, otherwise None.
        """
        digits = "".join(ch for ch in str(phone) if ch.isdigit())
        for phone_obj in self.phones:
            if phone_obj.value == digits:
                return phone_obj
        return None

    def remove_phone(self, phone: str) -> bool:
        """
        Remove a phone by its value.

        :param phone: Phone number to remove.
        :return: True if removed, False if not found.
        """
        target = self.find_phone(phone)
        if target is None:
            return False
        self.phones.remove(target)
        return True

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        """
        Replace an existing phone with a new one.

        :param old_phone: Existing phone number.
        :param new_phone: New phone number.
        :return: True if the phone was updated, False if old_phone was not found.
        """
        target = self.find_phone(old_phone)
        if target is None:
            return False
        new_phone_obj = Phone(new_phone)  # validation happens in Phone
        target.value = new_phone_obj.value
        return True

    # ---------- email / address / birthday ----------

    def add_email(self, email: str) -> None:
        """
        Add an email to the contact.

        Email validation is handled inside the Email class.

        :param email: Email address as a string.
        """
        self.emails.append(Email(email))

    def add_address(self, address: str) -> None:
        """
        Add an address to the contact.

        :param address: Address as a string.
        """
        self.addresses.append(Address(address))

    def add_birthday(self, birthday_str: str) -> None:
        """
        Set or update the birthday for the contact.

        :param birthday_str: Birthday in string form, e.g. '15.03.1990'.
        """
        self.birthday = Birthday(birthday_str)

    def show_birthday(self) -> Optional[str]:
        """
        Return the birthday formatted as DD.MM.YYYY.

        :return: Formatted birthday string or None if birthday is not set.
        """
        if not self.birthday:
            return None
        return self.birthday.value.strftime("%d.%m.%Y")

    # ---------- representation ----------

    def __str__(self) -> str:  # pragma: no cover
        """
        Return a human-readable representation of the contact.

        Example:
            Contact: John
            Phones: 0501234567, 0671234567
            Emails: john@gmail.com
            Addresses: Kyiv, Street 1
            Birthday: 15.03.1990
        """
        lines: List[str] = [f"Contact: {self.name.value}"]

        if self.phones:
            phones_str = ", ".join(phone.value for phone in self.phones)
            lines.append(f"Phones: {phones_str}")

        if self.emails:
            emails_str = ", ".join(email.value for email in self.emails)
            lines.append(f"Emails: {emails_str}")

        if self.addresses:
            addresses_str = ", ".join(address.value for address in self.addresses)
            lines.append(f"Addresses: {addresses_str}")

        birthday_str = self.show_birthday()
        if birthday_str:
            lines.append(f"Birthday: {birthday_str}")

        return "\n".join(lines)
