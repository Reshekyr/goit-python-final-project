from __future__ import annotations

from app.handlers import handlers as CONTACT_HANDLERS  # contact-related commands
from app.utils import parse_input
from app.memory import load_data, save_data  # adjust if your module name is different


def show_help() -> str:
    """
    Return formatted help text with all available commands
    grouped by category.
    """
    help_text = """
╔════════════════════════════════════╗
║  ПЕРСОНАЛЬНИЙ ПОМІЧНИК - ДОВІДКА   ║
╚════════════════════════════════════╝

📞 КОНТАКТИ:
  add [ім'я] [телефон]               - Додати контакт або телефон
  change [ім'я] [старий] [новий]     - Змінити телефон контакту
  delete [ім'я]                      - Видалити контакт
  phone [ім'я]                       - Показати телефони контакту
  all                                - Показати всі контакти
  search [запит]                     - Пошук контактів (ім'я/телефон)
  add-email [ім'я] [email]           - Додати email до контакту
  add-address [ім'я] [адреса]        - Додати адресу до контакту

🎂 ДНІ НАРОДЖЕННЯ:
  add-birthday [ім'я] [дата]         - Додати день народження (DD.MM.YYYY)
  show-birthday [ім'я]               - Показати день народження контакту
  birthdays [днів]                   - Майбутні дні народження (за замовчуванням 7)

📝 НОТАТКИ:
  add-note [title] [text]            - Додати нотатку
  show-notes                         - Показати всі нотатки
  find-note [запит]                  - Пошук нотаток за текстом/тегами
  edit-note [title] [new text]       - Редагувати нотатку
  delete-note [title]                - Видалити нотатку

🔧 ІНШЕ:
  hello                              - Привітання
  help                               - Показати цю довідку
  exit | close | quit                - Вийти з програми (зі збереженням даних)
"""
    return help_text.strip()


def main() -> None:
    """
    Entry point for CLI personal assistant.

    - Loads data on start
    - Runs main input loop
    - Dispatches commands to handlers
    - Saves data on exit
    """
    # Load data (contacts + notebook)
    contacts, notebook = load_data()  # type: ignore[assignment]
    print("Вітаємо у Персональному Помічнику!")
    print("Введіть 'help', щоб побачити список команд.\n")

    while True:
        user_input = input("Введіть команду: ").strip()

        # Skip empty input
        if not user_input:
            continue

        command, args = parse_input(user_input)

        # System / exit commands
        if command in ("exit", "close", "quit"):
            save_data(contacts, notebook)
            print("До побачення! Дані збережено.")
            break

        if command == "hello":
            print("Привіт! Чим я можу допомогти?")
            continue

        if command == "help":
            print(show_help())
            continue

        # Contact-related commands via handlers dict
        if command in CONTACT_HANDLERS:
            handler = CONTACT_HANDLERS[command]
            result = handler(args, contacts)
            if result:
                print(result)
            continue
        # Unknown command
        print("Невідома команда. Введіть 'help', щоб побачити доступні команди.")


if __name__ == "__main__":
    main()
