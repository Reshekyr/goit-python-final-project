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