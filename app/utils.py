from difflib import get_close_matches
from config import FUZZY_MATCH_CUTOFF, VALID_COMMANDS

def suggest_command(user_command: str) -> str:
    """Return a similar command for the given user input."""
    if not user_command:
        return ""
    return get_close_matches(user_command, VALID_COMMANDS, n=1, cutoff=FUZZY_MATCH_CUTOFF)[0]
