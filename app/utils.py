from difflib import get_close_matches
from typing import Dict, Callable

from app.config import FUZZY_MATCH_CUTOFF, VALID_COMMANDS, N_CLOSE_MATCHES



def suggest_command(user_command: str) -> list[str]:
    """Return a similar command for the given user input."""
    if not user_command:
        return ""
    return get_close_matches(user_command, VALID_COMMANDS, n=N_CLOSE_MATCHES, cutoff=FUZZY_MATCH_CUTOFF)


def parse_input(input_string: str) -> tuple[str, list[str]]:
    command, *args = input_string.split()
    return command.lower(), args

