#===
# Fuzzy matching configuration
#===
from typing import Callable, Dict

from app.handlers import hello, add_birthday, show_birthday, birthdays, add_note, show_notes, find_note, edit_note, \
    delete_note, add_tag, find_by_tag, show_tags, sort_by_tags, add_contact, get_phone, get_all, search_contacts, \
    change_phone, delete_contact, add_email, add_address

FUZZY_MATCH_CUTOFF = 0.6
VALID_COMMANDS = [
    # Contacts
    "add",
    "change",
    "phone",
    "all",
    "add-birthday",
    "birthdays",
    # Notes
    "add-note",
    "find-note",
    "delete-note",
    "edit-note",
    "list-notes",
    # General/other typical commands
    "hello",
    "close",
    "exit"
]
N_CLOSE_MATCHES = 1


#===
# JSON persistence configuration
#===
ADDRESSBOOK_FILE = "addressbook.json"
NOTEBOOK_FILE = "notebook.json"

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

    # contacts
    "add": add_contact,
    "phone": get_phone,
    "all": get_all,
    "search": search_contacts,
    "change": change_phone,
    "delete": delete_contact,
    "add-email": add_email,
    "add-address": add_address,
}
