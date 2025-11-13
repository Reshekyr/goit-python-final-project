import sys
from typing import Callable, Dict, Tuple

try:
    # If handlers are available in the project, leverage them
    from app.handlers import COMMANDS as HANDLERS  # type: ignore
except Exception:
    # Fallback to empty mapping when handlers are not present in the environment
    HANDLERS: Dict[str, Callable[..., str]] = {}

from app.suggestions import suggest_command, VALID_COMMANDS


def parse_input(user_input: str) -> Tuple[str, str]:
    """Split user input into (command, args_as_string)."""
    normalized = user_input.strip()
    if not normalized:
        return "", ""
    parts = normalized.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    return command, args


def main() -> None:
    print("Вітаю! Це персональний помічник. Введіть команду або 'help'.")
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
        if command in {"exit", "close", "quit"} or raw.lower() in {"good bye", "goodbye"}:
            print("До зустрічі!")
            break

        # If we have real handlers mapping, use it; otherwise, only provide suggestions
        if command in HANDLERS:
            try:
                handler = HANDLERS[command]
                result = handler(args) if args else handler()
                if result is not None:
                    print(result)
            except Exception as exc:
                print(f"Помилка виконання команди: {exc}")
            continue

        # Unknown command branch → suggest close matches
        suggestions = suggest_command(command)
        if suggestions:
            hint = ", ".join(suggestions)
            print(f"💡 Можливо: {hint}?")
        else:
            # If nothing close, show a generic help tip with known commands
            print("Невідома команда. Спробуйте 'help' або одну з відомих команд:")
            print(", ".join(sorted(set(VALID_COMMANDS))))


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Фатальна помилка: {err}", file=sys.stderr)
        sys.exit(1)


