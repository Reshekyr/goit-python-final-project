from collections import UserDict
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any


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

