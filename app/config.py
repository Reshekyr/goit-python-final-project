#===
# Fuzzy matching configuration
#===
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