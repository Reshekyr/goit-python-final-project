import re
import sys

# Глобальний список для зберігання email адрес
contacts_database = []

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def add_email_to_database(email):
    if not isinstance(email, str):
        print(f"[!] Некоректний тип даних. Додано 'Відсутня email-адреса'.")
        contacts_database.append("Відсутня email-адреса")
        return

    if not is_valid_email(email):
        print(f"[!] '{email}' не є дійсною адресою.")
        contacts_database.append("Відсутня email-адреса")
        return
        
    if email in contacts_database:
        print(f"[!] '{email}' вже присутній у списку. Додано 'Відсутня email-адреса'.")
        contacts_database.append("Відсутня email-адреса")
        return
        
    contacts_database.append(email)
    print(f"[+] '{email}' успішно додано.")

def display_emails():
    print("\n--- Список Email Адрес ---")
    if not contacts_database:
        print("Список порожній.")
    else:
        for index, email in enumerate(contacts_database):
            print(f"{index}: {email}")
    print("--------------------------")

def delete_email_by_index():
    display_emails()
    if not contacts_database:
        return

    try:
        index_str = input("Введіть номер (цифру) email, який потрібно видалити (або 'q' для скасування): ")
        if index_str.lower() == 'q':
            print("[i] Видалення скасовано.")
            return

        index = int(index_str)

        if 0 <= index < len(contacts_database):
            removed_email = contacts_database.pop(index)
            print(f"[+] '{removed_email}' (індекс {index}) успішно видалено.")
        else:
            print(f"[!] Некоректний індекс. Будь ласка, введіть число від 0 до {len(contacts_database)-1}.")
    except ValueError:
        print("[!] Некоректний ввід. Будь ласка, введіть потрібний порядковий номер для вибору.")

def edit_email_by_index():
    display_emails()
    if not contacts_database:
        return

    try:
        index_str = input("Введіть порядковий номер email, який потрібно редагувати (або 'q' для скасування): ")
        if index_str.lower() == 'q':
            print("[i] Редагування скасовано.")
            return

        index = int(index_str)

        if 0 <= index < len(contacts_database):
            old_email = contacts_database[index]
            new_email = input(f"Введіть нову адресу для '{old_email}': ")

            # Перевірка нового email перед оновленням
            if not is_valid_email(new_email):
                print(f"[!] '{new_email}' не є дійсною адресою. Залишено стару адресу.")
                return

            if new_email in contacts_database:
                print(f"[!] '{new_email}' вже присутній у списку. Залишено стару адресу.")
                return

            contacts_database[index] = new_email
            print(f"[+] Email оновлено: '{old_email}' -> '{new_email}'.")

        else:
            print(f"[!] Некоректний індекс. Будь ласка, введіть число від 0 до {len(contacts_database)-1}.")
    except ValueError:
        print("[!] Некоректний ввід. Будь ласка, введіть ціле число.")

# --- Основний цикл CLI програми ---

def main_menu():
    while True:
        print("\n=== Меню Управління Email ===")
        print("1. Додати email")
        print("2. Видалити email")
        print("3. Редагувати email")
        print("4. Переглянути список")
        print("5. Вийти")
        print("=============================")
        choice = input("Виберіть опцію (1-5): ")

        if choice == '1':
            email_input = input("Введіть email для додавання: ")
            add_email_to_database(email_input)
        elif choice == '2':
            delete_email_by_index()
        elif choice == '3':
            edit_email_by_index()
        elif choice == '4':
            display_emails()
        elif choice == '5':
            print("До побачення!")
            sys.exit()
        else:
            print("[!] Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":    
    main_menu()