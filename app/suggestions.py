from difflib import get_close_matches

# Centralized list of valid CLI commands.
# Keep this in sync with the actual supported commands in handlers/dispatcher.
# The list includes common aliases where relevant.
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
    "help",
    "close",
    "exit",
    "good bye",
    "goodbye",
    "quit",
]


def suggest_command(user_command: str) -> list[str]:
    """Return a list of up to 3 similar commands for the given user input."""
    if not user_command:
        return []
    return get_close_matches(user_command, VALID_COMMANDS, n=3, cutoff=0.6)


