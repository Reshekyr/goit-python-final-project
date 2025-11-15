import re

from collections import UserDict
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any

"""Notes module containing the Note class."""
class Note:
    """Represents a single note with title, content, creation time, and tags.

    Attributes:
        title: The title of the note (non-empty, stripped).
        content: The content/body of the note (non-empty, stripped).
        created_at: The datetime when the note was created.
        tags: A list of lowercase tags without duplicates.
    """
    def __init__(self, title: str, content: str):

        if not title or not title.strip():
            raise ValueError("title must not be empty")
        if not content or not content.strip():
            raise ValueError("content must not be empty")

        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.tags = []

    def add_tag(self, tag: str) -> None:
        """Add a lowercase tag if non-empty and not already present.

        Args:
            tag: The tag to add.
        """
        if tag is None:
            return
        normalized = tag.strip().lower()
        if not normalized:
            return
        if normalized not in self.tags:
            self.tags.append(normalized)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag if present.

        Args:
            tag: The tag to remove.
        """
        if tag is None:
            return
        normalized = tag.strip().lower()
        if not normalized:
            return
        try:
            self.tags.remove(normalized)
        except ValueError:
            # Tag not present; ignore
            pass

    def __str__(self) -> str:
        """Return a human-friendly string representation of the note."""
        timestamp = self.created_at.strftime("%d.%m.%Y %H:%M")
        header_line = f"[{timestamp}] {self.title}"
        body_line = self.content
        if self.tags:
            tags_line = f"Tags: {', '.join(self.tags)}"
            return f"{header_line}\n{body_line}\n{tags_line}"
        return f"{header_line}\n{body_line}"

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

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

        # Full Ukrainian number with country code
        if phone_number.startswith("380") and len(phone_number) > 10:
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
            

class Address(Field):
    """Class for storing contact address."""

    def __init__(self, value):
        super().__init__(value)


class Notebook:
    """A collection manager for Note objects keyed by their title.

    Notes are stored in an internal dictionary where keys are unique titles and
    values are Note-like objects with attributes: title, content, created_at, tags.
    """

    def __init__(self):
        """Initialize the notebook with an empty dictionary."""
        self._notes = {}

    def add_note(self, note):
        """Add a note to the notebook ensuring unique title.

        Args:
            note: A Note-like object with 'title' attribute.

        Raises:
            ValueError: If a note with the same title already exists.
        """
        key = note.title.strip() if getattr(note, "title", None) is not None else ""
        if not key:
            raise ValueError("note.title must not be empty")
        if key in self._notes:
            raise ValueError(f"Note with title '{key}' already exists")
        self._notes[key] = note

    def find_note(self, title):
        """Find a note by title.

        Args:
            title: The title of the note to find.

        Returns:
            The found note or None if not found.
        """
        key = title.strip()
        if not key:
            return None
        return self._notes.get(key)

    def delete_note(self, title):
        """Delete a note by title.

        Args:
            title: The title of the note to delete.

        Returns:
            True if the note was deleted, False if it did not exist.
        """
        if title is None:
            return False
        key = title.strip()
        if not key:
            return False
        return self._notes.pop(key, None) is not None

    def edit_note(self, title, new_content, update_created_at=False):
        """Edit a note's content. Optionally update its created_at timestamp.

        Args:
            title: The title of the note to edit.
            new_content: The new content for the note.
            update_created_at: If True, update created_at to now (optional).

        Returns:
            True if the note was edited, False if not found or invalid content.
        """
        note = self.find_note(title)
        if note is None:
            return False
        if new_content is None or not str(new_content).strip():
            return False
        note.content = str(new_content).strip()
        if update_created_at and hasattr(note, "created_at"):
            note.created_at = datetime.now()
        return True

    def search_notes(self, keyword):
        """Search notes by keyword in title and content (case-insensitive).

        Args:
            keyword: The search keyword.

        Returns:
            A list of matching notes.
        """
        if keyword is None:
            return []
        query = str(keyword).strip().lower()
        if not query:
            return []
        results = []
        for note in self._notes.values():
            title_text = str(getattr(note, "title", "")).lower()
            content_text = str(getattr(note, "content", "")).lower()
            if query in title_text or query in content_text:
                results.append(note)
        return results

    def show_all(self):
        """Return all notes as a list."""
        return list(self._notes.values())

    # ---- Tag-related (bonus) methods ----
    def find_by_tag(self, tag):
        """Find all notes that contain the specified tag (case-insensitive).

        Args:
            tag: The tag to search for.

        Returns:
            A list of notes that have the given tag.
        """
        if tag is None:
            return []
        needle = str(tag).strip().lower()
        if not needle:
            return []
        results = []
        for note in self._notes.values():
            tags = getattr(note, "tags", []) or []
            if needle in [t.lower() for t in tags]:
                results.append(note)
        return results

    def get_all_tags(self):
        """Get all unique tags across all notes as a sorted list."""
        unique = set()
        for note in self._notes.values():
            tags = getattr(note, "tags", []) or []
            for tag in tags:
                if isinstance(tag, str) and tag.strip():
                    unique.add(tag.strip().lower())
        return sorted(unique)

    def sort_by_tags(self, tag_list):
        """Return notes sorted by relevance to the provided tag list.

        Relevance is the number of matching tags between the note and tag_list.
        Notes with zero matches are excluded.

        Args:
            tag_list: Iterable of tags to match against.

        Returns:
            A list of notes sorted by descending number of tag matches; ties are
            broken by ascending title.
        """
        if not tag_list:
            return []
        query_tags = {str(t).strip().lower() for t in tag_list if str(t).strip()}
        if not query_tags:
            return []

        scored = []
        for note in self._notes.values():
            note_tags = {str(t).strip().lower() for t in (getattr(note, "tags", []) or []) if str(t).strip()}
            matches = len(note_tags & query_tags)
            if matches > 0:
                scored.append((matches, getattr(note, "title", ""), note))

        # Sort by matches desc, then by title asc for deterministic ordering
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [n for _, __, n in scored]
        # Check that address is not empty
        if not value or not value.strip():
            raise ValueError("Address cannot be empty")

        # Remove leading and trailing whitespace
        super().__init__(value.strip())

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

        # Full Ukrainian number with country code
        if phone_number.startswith("380") and len(phone_number) > 10:
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

class Email(Field):
    def __init__(self):
        self.contacts_database = []
        self.pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def _load_data(self):
        return []

    def _save_data(self):
        pass

    def is_valid_email(self, email):
        return bool(re.match(self.pattern, email))

    def add_email(self, email):
        if not isinstance(email, str):
            print(f"[!] Некоректний тип даних.")
            return

        if not self.is_valid_email(email):
            print(f"[!] '{email}' не є дійсною адресою.")
            return
            
        if email in self.contacts_database:
            print(f"[!] '{email}' вже присутній у списку.")
            return
            
        self.contacts_database.append(email)
        print(f"[+] '{email}' успішно додано.")
        self._save_data()

    def display_emails(self):
        print("\n--- Список Email Адрес ---")
        if not self.contacts_database:
            print("Список порожній.")
        else:
            for index, email in enumerate(self.contacts_database):
                print(f"{index}: {email}")
        print("--------------------------")

    def delete_email_by_index(self):
        self.display_emails()
        if not self.contacts_database:
            return

        try:
            index_str = input("Введіть номер email, який потрібно видалити (або 'q' для скасування): ")
            if index_str.lower() == 'q':
                print("[i] Видалення скасовано.")
                return

            index = int(index_str)

            if 0 <= index < len(self.contacts_database):
                removed_email = self.contacts_database.pop(index)
                print(f"[+] '{removed_email}' (індекс {index}) успішно видалено.")
                self._save_data() # Цей виклик тепер нічого не робить
            else:
                print(f"[!] Некоректний індекс. Будь ласка, введіть порядковий номер від 0 до {len(self.contacts_database)-1}.")
        except ValueError:
            print("[!] Некоректний ввід. Будь ласка, введіть потрібний порядковий номер для вибору.")

    def edit_email_by_index(self):
        self.display_emails()
        if not self.contacts_database:
            return

        try:
            index_str = input("Введіть порядковий номер email, який потрібно редагувати (або 'q' для скасування): ")
            if index_str.lower() == 'q':
                print("[i] Редагування скасовано.")
                return

            index = int(index_str)

            if 0 <= index < len(self.contacts_database):
                old_email = self.contacts_database[index]
                new_email = input(f"Введіть нову адресу для '{old_email}': ")

                if not self.is_valid_email(new_email):
                    print(f"[!] '{new_email}' не є дійсною адресою. Залишено стару адресу.")
                    return

                if new_email in self.contacts_database:
                    print(f"[!] '{new_email}' вже присутній у списку. Залишено стару адресу.")
                    return

                self.contacts_database[index] = new_email
                print(f"[+] Email оновлено: '{old_email}' -> '{new_email}'.")
                self._save_data()

            else:
                print(f"[!] Некоректний індекс. Будь ласка, введіть число від 0 до {len(self.contacts_database)-1}.")
        except ValueError:
            print("[!] Некоректний ввід. Будь ласка, введіть ціле число.")

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

