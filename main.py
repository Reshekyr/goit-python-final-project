import sys
from typing import Tuple

from app.memory import load_data, save_data
from app.utils import parse_input
from app.config import handlers, VALID_COMMANDS

from app.utils import suggest_command


def parse_input(user_input: str) -> Tuple[str, str]:
    """Split user input into (command, args_as_string)."""
    normalized = user_input.strip()
    if not normalized:
        return "", ""
    parts = normalized.split()
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else ""
    return command, args


def main() -> None:
    print("Вітаю! Це персональний помічник. Введіть команду.")
    address_book = load_data()
    while True:
        try:
            raw = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nДо зустрічі!")
            break

        command, args = parse_input(raw)
        if not command:
            continue

        # Exit/close aliases handled early
        if command in {"exit", "close", "quit"} or raw.lower() in {
            "good bye",
            "goodbye",
        }:
            print("До зустрічі!")
            break

        # If we have real handlers mapping, use it; otherwise, only provide suggestions
        if command in handlers:
            handler = handlers[command]
            result = handler(args, address_book)
            if result is not None:
                print(result)
        else:
            # Unknown command branch → suggest close matches
            suggestions = suggest_command(command)
            if suggestions:
                hint = ", ".join(suggestions)
                print(f"💡 Можливо: {hint}?")
            else:
                # If nothing close, show a generic help tip with known commands
                print("Невідома команда. Спробуйте 'help' або одну з відомих команд:")
                print(", ".join(sorted(set(VALID_COMMANDS))))
    save_data(address_book)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Фатальна помилка: {err}", file=sys.stderr)
        sys.exit(1)
