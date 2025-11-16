from typing import List
from app.decorators import input_error
from app.entities import AddressBook, Record, Note


# -----------------------------
# Basic helper/utility handlers
# -----------------------------
def hello(*_) -> str:
    """
    Returns a greeting message.
    """
    return "Чим можу тобі допомогти?"


# --------------------------------
# Contacts: birthdays functionality
# --------------------------------
@input_error
def add_birthday(args: List[str], contacts) -> str:
    """
    Adds a birthday to a contact.

    Command:
        add-birthday [name] [date]
    Date format: DD.MM.YYYY
    """
    if len(args) < 2:
        raise ValueError("Будь ласка, введіть ім'я та дату у форматі DD.MM.YYYY")

    contact_name, date_str = args[0], args[1]

    record = contacts.find(contact_name)
    if record is None:
        record = contacts.add_record(contact_name)

    # Validation happens inside the Birthday class/add_birthday method
    record.add_birthday(date_str)
    return f"✅ День народження додано до контакту {contact_name}"


@input_error
def show_birthday(args: List[str], contacts) -> str:
    """
    Shows the birthday of a contact.

    Command:
        show-birthday [name]
    """
    if not args:
        raise ValueError("Будь ласка, надайте ім'я контакту")

    contact_name = args[0]
    record = contacts.find(contact_name)
    if record is None:
        raise ValueError(f"Контакт '{contact_name}' не знайдено")

    bday_str = record.show_birthday()

    return f"День народження {contact_name}: {bday_str}"


@input_error
def birthdays(args: List[str], contacts) -> str:
    """
    Shows upcoming birthdays.

    Command:
        birthdays [number_of_days]
    Default number of days = 7.
    """
    days = 7
    if args:
        days = int(args[0])

    upcoming = contacts.get_upcoming_birthdays(days)
    if not upcoming:
        return "Немає днів народження у найближчий період"

    lines: List[str] = [f"Дні народження протягом наступних {days} днів:"]
    for item in upcoming:
        # Expected structure: {'name', 'birthday', 'congratulation_date'}
        name = item.get("name")
        birthday = item.get("birthday")
        congrats = item.get("congratulation_date")

        # Support for datetime.date/datetime.datetime, as well as already formatted strings
        def fmt(d) -> str:
            if hasattr(d, "strftime"):
                return d.strftime("%d.%m.%Y")
            return str(d)

        lines.append(f"   {name}: {fmt(birthday)} (congratulate: {fmt(congrats)})")

    return "\n".join(lines)


# ----------------
# Notes management
# ----------------


@input_error
def add_note(args: List[str], contacts) -> str:
    """
    Creates a new note.

    Command:
        add-note [name] [title] [text...]
    """
    if len(args) < 2:
        raise ValueError("Будь ласка, вкажіть заголовок та вміст нотатки")

    name = args[0]
    record = contacts.find(name)
    notebook = record.notebook
    title = args[1]
    content = " ".join(args[2:])

    note = Note(title, content)

    notebook.add_note(note)
    return f"Note '{title}' created"


def show_notes(args: List[str], contacts) -> str:
    """
    Shows all notes (without decorator, as an exception from the requirements).

    Command:
        show-notes
    """
    name = args[0]
    record = contacts.find(name)
    notebook = record.notebook
    all_notes = notebook.show_all()
    if not all_notes:
        return "Нотатки відсутні"

    lines: List[str] = [f"All notes ({len(all_notes)}):"]
    separator = "—" * 3

    for n in all_notes:
        # Support for different formats: note object or string/dictionary
        if hasattr(n, "created_at") and hasattr(n, "title") and hasattr(n, "content"):
            created = getattr(n, "created_at")
            created_str = (
                created.strftime("%d.%m.%Y %H:%M")
                if hasattr(created, "strftime")
                else str(created)
            )
            title = getattr(n, "title")
            content = getattr(n, "content")
        elif isinstance(n, dict):
            created_str = str(n.get("created_at", ""))
            title = n.get("title", "")
            content = n.get("content", "")
        else:
            # Fallback: convert to string
            created_str = ""
            title = str(n)
            content = ""

        header = f"[{created_str}] {title}".strip()
        lines.append(f"   {header}")
        if content:
            lines.append(f"   {content}")
        lines.append(f"   {separator}")

    return "\n".join(lines)


@input_error
def find_note(args: List[str], contacts) -> str:
    """
    Search notes by a keyword.

    Command:
        find-note [keyword]
    """
    if not args:
        raise ValueError("Будь ласка, надайте ключове слово для пошуку")
    name = args[0]
    keyword = args[1]
    record = contacts.find(name)
    notebook = record.notebook
    results = notebook.search_notes(keyword)

    if not results:
        return "Нічого не знайдено"

    lines: List[str] = [f"Found {len(results)} notes:"]
    for n in results:
        created = n.created_at
        created_str = created.strftime("%d.%m.%Y %H:%M")
        title = n.title
        content = n.content
        lines.append(f"   [{created_str}] {title}\n   {content}")

    return "\n".join(lines)


@input_error
def edit_note(args: List[str], contacts) -> str:
    """
    Edits the content of a note.

    Command:
        edit-note [title] [new_text...]
    """
    if len(args) < 2:
        raise ValueError("Будь ласка, вкажіть заголовок та новий текст")
    name = args[0]
    title = args[1]
    new_content = " ".join(args[2:])
    record = contacts.find(name)
    notebook = record.notebook
    notebook.edit_note(title, new_content)
    return f"Нотатка '{title}' оновлена"


@input_error
def delete_note(args: List[str], contacts) -> str:
    """
    Deletes a note.

    Command:
        delete-note [title]
    """
    if not args:
        raise ValueError("Будь ласка, вкажіть заголовок нотатки")
    name = args[0]
    title = args[1]
    record = contacts.find(name)
    notebook = record.notebook
    notebook.delete_note(title)
    return f"Нотатка '{title}' видалена"


# ---------------------------
# Notes tags (extra features)
# ---------------------------
@input_error
def add_tag(args: List[str], contacts) -> str:
    """
    Adds a tag to a note.

    Command:
        add-tag [title] [tag]
    """
    if len(args) < 2:
        raise ValueError("Будь ласка, вкажіть заголовок нотатки та тег")

    name, title, tag = args[0], args[1], args[2]
    record = contacts.find(name)
    notebook = record.notebook
    note = notebook.find_note(title)
    note.add_tag(tag)
    return f"Тег '{tag}' додано до нотатки '{title}'"


@input_error
def find_by_tag(args: List[str], contacts) -> str:
    """
    Search notes by a tag.

    Command:
        find-by-tag [tag]
    """
    if not args:
        raise ValueError("Будь ласка, вкажіть тег для пошуку")
    name = args[0]
    tag = args[1]
    record = contacts.find(name)
    notebook = record.notebook
    results = notebook.find_by_tag(tag)
    if not results:
        return "Нічого не знайдено"

    lines: List[str] = [f"Знайдено {len(results)} нотатки:"]
    for n in results:
        lines.append(f"   {n.title}")
    return "\n".join(lines)


@input_error
def show_tags(args: List[str], contacts) -> str:
    """
    Returns all unique tags.

    Command:
        show-tags
    """
    name = args[0]
    record = contacts.find(name)
    notebook = record.notebook
    tags = notebook.get_all_tags()
    if not tags:
        return "Немає тегів"
    return "Tags: " + ", ".join(sorted(tags))


@input_error
def sort_by_tags(args: List[str], contacts) -> str:
    """
    Sorts notes by relevance to the specified tags.

    Command:
        sort-by-tags [tag1] [tag2] ...
    """
    if not args:
        raise ValueError("Будь ласка, вкажіть принаймні один тег для сортування")
    name = args[0]
    record = contacts.find(name)
    notebook = record.notebook
    sorted_notes = notebook.sort_by_tags(args[1:])
    if not sorted_notes:
        return "Нотатки відсутні"

    lines: List[str] = ["Sorted notes:"]
    for n in sorted_notes:
        lines.append(f"   {n.title}")
    return "\n".join(lines)


# ---------------------------
# Basic commands for contacts
# ---------------------------


@input_error
def add_contact(args: list[str], contacts: AddressBook) -> str:
    """Add a new contact or phone to existing contact"""
    if len(args) < 2:
        raise ValueError("Недостатньо аргументів. Usage: add [name] [phone]")

    contact_name, contact_phone_number = args[0], args[1]
    record = contacts.find(contact_name)
    if record is None:
        record = Record(contact_name)
        contacts.add_record(record)

    record.add_phone(contact_phone_number)
    return f"✅ Контакт {contact_name} додано успішно"


@input_error
def get_phone(args: list[str], contacts: AddressBook) -> str:
    """Show all phones of a contact"""
    if len(args) < 1:
        raise ValueError("Недостатньо аргументів. Usage: phone [name]")

    contact_name = args[0]
    record = contacts.find(contact_name)

    if record is None:
        raise KeyError(f"❌ Контакт {contact_name} не знайдено")

    if not record.phones:
        return f"📭 Контакт {contact_name} немає телефонів"

    phones_str = ", ".join(phone.value for phone in record.phones)
    plural = "s" if len(record.phones) > 1 else ""
    return f"📞 Контакт {contact_name} телефон {plural}: {phones_str}"


@input_error
def get_all(_: list[str], contacts: AddressBook) -> str:
    """Show all contacts with full information"""
    result: list[str] = []

    if not contacts.data:
        return "📭 Контакти не знайдено"

    for contact_name, record in contacts.data.items():
        # Phones
        phones_str = (
            ", ".join(phone.value for phone in record.phones)
            if record.phones
            else "телефони відсутні"
        )

        # Birthday
        birthday_str = (
            f" - Birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
            if record.birthday and record.birthday.value
            else ""
        )

        # Emails (list)
        emails_str = (
            f" - Emails: {', '.join(email.value for email in record.emails)}"
            if record.emails
            else " - no emails"
        )

        # Addresses (list)
        addresses_str = (
            f" - Addresses: {', '.join(address.value for address in record.addresses)}"
            if record.addresses
            else " - no addresses"
        )

        result.append(
            f"👤 {contact_name} - {phones_str}{birthday_str}{emails_str}{addresses_str}"
        )

    return "\n".join(result)


@input_error
def search_contacts(args: list, contacts: AddressBook) -> str:
    """Search contacts by name or phone number"""
    if len(args) < 1:
        raise ValueError("Недостатньо аргументів. Usage: search [query]")

    query = args[0]
    results = contacts.search(query)

    if not results:
        return f"🔍 За вашим запитом нічого не знайдено '{query}'"

    result_lines = [f"🔍 Знайдено контактів: {len(results)}"]

    for record in results:
        phones = [phone.value for phone in record.phones]
        phones_str = ", ".join(phones) if phones else "no phones"
        result_lines.append(f"👤 {record.name.value}: {phones_str}")

    return "\n".join(result_lines)


@input_error
def change_phone(args: list[str], contacts: AddressBook) -> str:
    """Change phone number of existing contact"""
    if len(args) < 3:
        raise ValueError(
            "Недостатньо аргументів. Usage: change [name] [old_phone] [new_phone]"
        )

    contact_name, old_phone_number, new_phone_number = args[0], args[1], args[2]
    record = contacts.find(contact_name)

    if record is None:
        raise KeyError(f"❌ Contact {contact_name} not found")

    if record.edit_phone(old_phone_number, new_phone_number):
        return f"✅ Контакт {contact_name} успішно оновлено"
    else:
        raise ValueError(
            f"Телефон {old_phone_number} не знайдено до контакту {contact_name}"
        )


@input_error
def delete_contact(args: list, contacts: AddressBook) -> str:
    """Delete a contact by name"""
    if len(args) < 1:
        raise ValueError("Недостатньо аргументів. Usage: delete [name]")

    name = args[0]
    record = contacts.find(name)

    if record is None:
        raise KeyError(f"❌ Контакт {name} не знайдено")

    contacts.delete(name)
    return f"✅ Контакт {name} видалено успішно"


@input_error
def add_email(args: list, contacts: AddressBook) -> str:
    """Add email to existing contact"""
    if len(args) < 2:
        raise ValueError("Недостатньо аргументів. Usage: add-email [name] [email]")

    name, email = args[0], args[1]
    record = contacts.find(name)

    if record is None:
        raise KeyError(f"❌ Контакт {name} не знайдено")

    record.add_email(email)
    return f"✅ Email успішно додано до контакту {name}"


@input_error
def add_address(args: list, contacts: AddressBook) -> str:
    """Add address to existing contact"""
    if len(args) < 2:
        raise ValueError("Недостатньо аргументів. Usage: add-address [name] [address...]")

    name = args[0]
    address = " ".join(args[1:])
    record = contacts.find(name)

    if record is None:
        raise KeyError(f"❌ Контакт {name} не знайдено")

    record.add_address(address)
    return f"✅ Адреса додана успішно до контакту {name}"
