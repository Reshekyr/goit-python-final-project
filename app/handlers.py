
from collections import defaultdict
from typing import Callable, Dict, List, Optional

from .decorators import input_error


# -----------------------------
# Basic helper/utility handlers
# -----------------------------
def hello(_: List[str], __) -> str:
    """
    Returns a greeting message.
    """
    return "How can I help you?"


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
        raise ValueError("Please provide a name and date in the format DD.MM.YYYY")

    contact_name, date_str = args[0], args[1]

    record = contacts.find(contact_name)
    if record is None:
        record = contacts.add_record(contact_name)

    # Validation happens inside the Birthday class/add_birthday method
    record.add_birthday(date_str)
    return f"Birthday added to contact {contact_name}"


@input_error
def show_birthday(args: List[str], contacts) -> str:
    """
    Shows the birthday of a contact.

    Command:
        show-birthday [name]
    """
    if not args:
        raise ValueError("Please provide a name of a contact")

    contact_name = args[0]
    record = contacts.find(contact_name)
    if record is None:
        raise ValueError(f"Contact '{contact_name}' not found")

    bday_str = record.show_birthday()

    return f"Birthday of {contact_name}: {bday_str}"


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
        return "No birthdays in the upcoming period"

    lines: List[str] = [f"Birthdays in the next {days} days:"]
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
def add_note(args: List[str], notebook) -> str:
    """
    Creates a new note.

    Command:
        add-note [title] [text...]
    """
    if len(args) < 2:
        raise ValueError("Please provide a title and content of the note")

    title = args[0]
    content = " ".join(args[1:])

    note = Note(title, content)

    notebook.add_note(note)
    return f"Note '{title}' created"


def show_notes(_: List[str], notebook) -> str:
    """
    Shows all notes (without decorator, as an exception from the requirements).

    Command:
        show-notes
    """
    all_notes = notebook.show_all()
    if not all_notes:
        return "No notes"

    lines: List[str] = [f"All notes ({len(all_notes)}):"]
    separator = "—" * 3

    for n in all_notes:
        # Підтримка різних форматів: об'єкт нотатки або рядок/словник
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
            # Фолбек: перетворити в рядок
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
def find_note(args: List[str], notebook) -> str:
    """
    Search notes by a keyword.

    Command:
        find-note [keyword]
    """
    if not args:
        raise ValueError("Please provide a keyword for the search")
    keyword = args[0]
    results = notebook.search_notes(keyword)

    if not results:
        return "Nothing found"

    lines: List[str] = [f"Found {len(results)} notes:"]
    for n in results:
        created = n.created_at
        created_str = created.strftime("%d.%m.%Y %H:%M")
        title = n.title
        content = n.content
        lines.append(f"   [{created_str}] {title}\n   {content}")

    return "\n".join(lines)


@input_error
def edit_note(args: List[str], notebook) -> str:
    """
    Edits the content of a note.

    Command:
        edit-note [title] [new_text...]
    """
    if len(args) < 2:
        raise ValueError("Please provide a title and new text")

    title = args[0]
    new_content = " ".join(args[1:])
    notebook.edit_note(title, new_content)
    return f"Note '{title}' updated"


@input_error
def delete_note(args: List[str], notebook) -> str:
    """
    Deletes a note.

    Command:
        delete-note [title]
    """
    if not args:
        raise ValueError("Please provide a title of the note")
    title = args[0]
    notebook.delete_note(title)
    return f"Note '{title}' deleted"


# ---------------------------
# Notes tags (extra features)
# ---------------------------
@input_error
def add_tag(args: List[str], notebook) -> str:
    """
    Adds a tag to a note.

    Command:
        add-tag [title] [tag]
    """
    if len(args) < 2:
        raise ValueError("Please provide a title and tag of the note")
    title, tag = args[0], args[1]
    notebook.add_tag(title, tag)
    return f"Tag '{tag}' added to note '{title}'"


@input_error
def find_by_tag(args: List[str], notebook) -> str:
    """
    Search notes by a tag.

    Command:
        find-by-tag [tag]
    """
    if not args:
        raise ValueError("Please provide a tag")
    tag = args[0]
    results = notebook.find_by_tag(tag)
    if not results:
        return "Nothing found"

    lines: List[str] = [f"Found {len(results)} notes:"]
    for n in results:
        lines.append(f"   {n.title}")
    return "\n".join(lines)


@input_error
def show_tags(_: List[str], notebook) -> str:
    """
    Returns all unique tags.

    Command:
        show-tags
    """
    tags = notebook.get_all_tags()
    if not tags:
        return "No tags"
    return "Tags: " + ", ".join(sorted(tags))


@input_error
def sort_by_tags(args: List[str], notebook) -> str:
    """
    Sorts notes by relevance to the specified tags.

    Command:
        sort-by-tags [tag1] [tag2] ...
    """
    if not args:
        raise ValueError("Please provide at least one tag")
    sorted_notes = notebook.sort_by_tags(args)
    if not sorted_notes:
        return "No notes found"

    lines: List[str] = ["Sorted notes:"]
    for n in sorted_notes:
        lines.append(f"   {n.title}")
    return "\n".join(lines)


# ----------------
# Handlers mapping
# ----------------
handlers: Dict[str, Callable] = {
    # base
    "hello": hello,
    
    # birthdays
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    
    # notes
    "add-note": add_note,
    "show-notes": show_notes,
    "find-note": find_note,
    "edit-note": edit_note,
    "delete-note": delete_note,
    
    # tags (extra)
    "add-tag": add_tag,
    "find-by-tag": find_by_tag,
    "show-tags": show_tags,
    "sort-by-tags": sort_by_tags,
}

