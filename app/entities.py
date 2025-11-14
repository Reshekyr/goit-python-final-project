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


class AddressBook(UserDict):
    """
    Address book for storing and managing contact records.

    Internally uses a dictionary:
        key   -> contact name (str)
        value -> Record instance
    """

    # ---------- CRUD ----------

    def add_record(self, record) -> None:
        """
        Add a new contact record to the address book.

        Name uniqueness is enforced case-insensitively.

        :param record: Record instance to add.
        :raises ValueError: if a contact with the same name already exists.
        """
        name = record.name.value
        if self._has_name(name):
            raise ValueError(f"Contact with name '{name}' already exists.")
        self.data[name] = record

    def find(self, name: str):
        """
        Find a contact by name (case-insensitive).

        :param name: Name to search for.
        :return: Record if found, otherwise None.
        """
        target = name.casefold()
        for stored_name, record in self.data.items():
            if stored_name.casefold() == target:
                return record
        return None

    def delete(self, name: str) -> bool:
        """
        Delete a contact by name (case-insensitive).

        :param name: Name of the contact to delete.
        :return: True if the contact was found and deleted, False otherwise.
        """
        target = name.casefold()
        for stored_name in list(self.data.keys()):
            if stored_name.casefold() == target:
                del self.data[stored_name]
                return True
        return False

    # ---------- SEARCH ----------

    def search(self, query: str):
        """
        Search contacts by partial, case-insensitive match.

        The search is performed across:
        - name
        - phone numbers
        - emails (list)
        - addresses (list)

        :param query: Search string.
        :return: List of matching records.
        """
        q = query.casefold()
        results = []

        for record in self.data.values():
            fields = self._collect_search_fields(record)
            if any(q in field for field in fields):
                results.append(record)

        return results

    # ---------- BIRTHDAYS ----------

    def get_upcoming_birthdays(self, days: int = 7) -> List[Dict[str, str]]:
        """
        Get a list of upcoming birthdays within the next `days` days.

        If a birthday falls on a weekend (Saturday/Sunday), the
        congratulation date is moved to the following Monday.

        Each result item has the following structure:
            {
                "name": "John",
                "birthday": "15.03.1990",
                "congratulation_date": "17.03.2025"
            }

        :param days: Number of days to look ahead (default 7).
        :return: List of dictionaries with birthday information.
        """
        today = date.today()
        window_end = today + timedelta(days=days)
        result: List[Dict[str, str]] = []

        for record in self.data.values():
            birthday = self._get_birthday_date(record)
            if birthday is None:
                continue

            # Birthday in the current year
            birthday_this_year = birthday.replace(year=today.year)

            # If already passed this year, use the next year
            if birthday_this_year < today:
                next_birthday = birthday.replace(year=today.year + 1)
            else:
                next_birthday = birthday_this_year

            # Check if next birthday is inside the window
            if today <= next_birthday <= window_end:
                congratulation_date = self._move_weekend_to_monday(next_birthday)

                result.append(
                    {
                        "name": record.name.value,
                        "birthday": birthday.strftime("%d.%m.%Y"),
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        # Sort by congratulation date and then by name
        result.sort(
            key=lambda item: (
                datetime.strptime(item["congratulation_date"], "%d.%m.%Y"),
                item["name"].casefold(),
            )
        )
        return result

    # ---------- Helper methods ----------

    def _has_name(self, name: str) -> bool:
        """
        Check if a contact with the given name already exists
        (case-insensitive).
        """
        target = name.casefold()
        return any(stored.casefold() == target for stored in self.data.keys())

    @staticmethod
    def _get_birthday_date(record) -> Optional[date]:
        """
        Extract birthday date from a record.

        Expects:
            record.birthday is either:
            - None
            - an object with .value: date

        :param record: Record instance.
        :return: date if exists, otherwise None.
        """
        if not record.birthday:
            return None
        return record.birthday.value

    @staticmethod
    def _move_weekend_to_monday(day: date) -> date:
        """
        If the given date falls on a weekend (Saturday=5, Sunday=6),
        move it to the next Monday. Otherwise, return the date unchanged.

        :param day: Original date.
        :return: Adjusted date.
        """
        weekday = day.weekday()
        if weekday == 5:  # Saturday
            return day + timedelta(days=2)
        if weekday == 6:  # Sunday
            return day + timedelta(days=1)
        return day

    @staticmethod
    def _normalize_value(value: Any) -> str:
        """
        Normalize a value to a lowercase string for search.

        Supports:
        - plain strings
        - objects with .value: str
        """
        if value is None:
            return ""
        if hasattr(value, "value"):
            return str(value.value).casefold()
        return str(value).casefold()

    def _collect_search_fields(self, record) -> List[str]:
        """
        Collect all searchable fields from a record and normalize them
        to lowercase strings for case-insensitive matching.

        Fields included:
        - name
        - all phone numbers
        - all emails
        - all addresses

        :param record: Record instance.
        :return: List of normalized strings.
        """
        # Name (required, single)
        fields: List[str] = [record.name.value.casefold()]

        # Phones: list[Phone] with .value
        fields += [phone.value.casefold() for phone in record.phones]

        # Emails: list of strings or objects with .value
        emails = getattr(record, "emails", [])
        fields += [self._normalize_value(email) for email in emails]

        # Addresses: list of strings or objects with .value
        addresses = getattr(record, "addresses", [])
        fields += [self._normalize_value(address) for address in addresses]

        return fields


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
