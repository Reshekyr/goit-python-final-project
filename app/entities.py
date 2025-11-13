import re
import sys
import json
import pickle
import os

JSON_FILE = "contacts.json"
PICKLE_FILE = "contacts.pkl"

contacts_database = []

def save_data():
    """Зберігає поточну базу даних у JSON і робить бекап у Pickle."""
    try:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts_database, f, ensure_ascii=False, indent=4)
        print(f"[i] Дані успішно збережено у {JSON_FILE}")
    except IOError as e:
        print(f"[!] Помилка збереження JSON файлу: {e}")

    try:
        with open(PICKLE_FILE, 'wb') as f:
            pickle.dump(contacts_database, f)
        print(f"[i] Резервну копію успішно збережено у {PICKLE_FILE}")
    except IOError as e:
        print(f"[!] Помилка збереження файлу резервної копії (Pickle): {e}")

def load_data():
    global contacts_database
    
    # Спочатку пробуємо завантажити з JSON
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                contacts_database = json.load(f)
            print(f"[i] Дані успішно завантажено з {JSON_FILE}")
            return
        except (IOError, json.JSONDecodeError) as e:
            print(f"[!] Помилка завантаження JSON файлу: {e}. Спроба завантаження з резервної копії.")

    # Якщо JSON не спрацював, пробуємо Pickle
    if os.path.exists(PICKLE_FILE):
        try:
            with open(PICKLE_FILE, 'rb') as f:
                contacts_database = pickle.load(f)
            print(f"[i] Дані успішно завантажено з {PICKLE_FILE} (резервна копія)")
            return
        except (IOError, pickle.UnpicklingError) as e:
            print(f"[!] Помилка завантаження файлу резервної копії (Pickle): {e}.")
            
    print("[i] Файли даних не знайдено. Розпочато чистий сеанс.")

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def add_email_to_database(email):
    if not isinstance(email, str):
        print(f"[!] Некоректний тип даних. Додано 'Відсутня email-адреса'.")
        contacts_database.append("Відсутня email-адреса")
        save_data()
        return

    if not is_valid_email(email):
        print(f"[!] '{email}' не є дійсною адресою.")
        contacts_database.append("Відсутня email-адреса")
        save_data()
        return
        
    if email in contacts_database:
        print(f"[!] '{email}' вже присутній у списку. Додано 'Відсутня email-адреса'.")
        contacts_database.append("Відсутня email-адреса")
        save_data()
        return
        
    contacts_database.append(email)
    print(f"[+] '{email}' успішно додано.")
    save_data()

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
        index_str = input("Введіть номер email, який потрібно видалити (або 'q' для скасування): ")
        if index_str.lower() == 'q':
            print("[i] Видалення скасовано.")
            return

        index = int(index_str)

        if 0 <= index < len(contacts_database):
            removed_email = contacts_database.pop(index)
            print(f"[+] '{removed_email}' (індекс {index}) успішно видалено.")
            save_data()
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

            if not is_valid_email(new_email):
                print(f"[!] '{new_email}' не є дійсною адресою. Залишено стару адресу.")
                return

            if new_email in contacts_database:
                print(f"[!] '{new_email}' вже присутній у списку. Залишено стару адресу.")
                return

            contacts_database[index] = new_email
            print(f"[+] Email оновлено: '{old_email}' -> '{new_email}'.")
            save_data()

        else:
            print(f"[!] Некоректний індекс. Будь ласка, введіть число від 0 до {len(contacts_database)-1}.")
    except ValueError:
        print("[!] Некоректний ввід. Будь ласка, введіть ціле число.")

def main_menu():
    load_data() 
    
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
            print("До побачення! (Дані вже збережено)")
            sys.exit()
        else:
            print("[!] Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main_menu()
