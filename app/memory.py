import json
from json import JSONDecodeError
from typing import Tuple, Any, Dict

from entities import AddressBook, Notebook
from config import ADDRESSBOOK_FILE, NOTEBOOK_FILE



def _count_from_dict(data: Dict[str, Any], key: str) -> int:
    """Safely count list entries for given key in a dict."""
    value = data.get(key, [])
    if isinstance(value, list):
        return len(value)
    return 0


def save_data(address_book: Any, notebook: Any) -> None:
    """
    Save address book and notebook to JSON files.
    
    Args:
        address_book: AddressBook object
        notebook: Notebook object

    Returns:
        None

    Raises:
        OSError: If there is an error saving the data
        TypeError: If there is an error saving the data
        ValueError: If there is an error saving the data
    """
    # Save AddressBook
    try:
        book_dict = address_book.to_dict() if hasattr(address_book, "to_dict") else {}
        count_contacts = _count_from_dict(book_dict if isinstance(book_dict, dict) else {}, "contacts")
        with open(ADDRESSBOOK_FILE, "w", encoding="utf-8") as f:
            json.dump(book_dict, f, ensure_ascii=False, indent=2)
        print(f"Дані контактів збережено до '{ADDRESSBOOK_FILE}' (записів: {count_contacts})")
    except (OSError, TypeError, ValueError) as e:
        print(f"Помилка збереження '{ADDRESSBOOK_FILE}': {e}")

    # Save Notebook
    try:
        nb_dict = notebook.to_dict() if hasattr(notebook, "to_dict") else {}
        count_notes = _count_from_dict(nb_dict if isinstance(nb_dict, dict) else {}, "notes")
        with open(NOTEBOOK_FILE, "w", encoding="utf-8") as f:
            json.dump(nb_dict, f, ensure_ascii=False, indent=2)
        print(f"Дані нотаток збережено до '{NOTEBOOK_FILE}' (записів: {count_notes})")
    except (OSError, TypeError, ValueError) as e:
        print(f"Помилка збереження '{NOTEBOOK_FILE}': {e}")


def load_data() -> Tuple[Any, Any]:
    """
    Load address book and notebook from JSON files.
    
    Returns:
        Tuple[Any, Any]: Tuple containing AddressBook and Notebook objects

    Raises:
        FileNotFoundError: If the address book file is not found
        JSONDecodeError: If the address book file is not valid JSON
        Exception: If there is an error loading the data
    """
    try:
        with open(ADDRESSBOOK_FILE, "r", encoding="utf-8") as f:
            book_data = json.load(f)
        # Recreate object using from_dict if available
        address_book = AddressBook.from_dict(book_data)
        contacts_loaded = len(address_book.data)
        print(f"Завантажено контактів: {contacts_loaded}")
    except FileNotFoundError:
        address_book = AddressBook() if isinstance(AddressBook, type) else {}
        print(f"ℹФайл '{ADDRESSBOOK_FILE}' не знайдено. Створено порожню адресну книгу.")
    except JSONDecodeError as e:
        address_book = AddressBook() if isinstance(AddressBook, type) else {}
        print(f"Помилка читання '{ADDRESSBOOK_FILE}': некоректний JSON ({e}). Створено порожню адресну книгу.")
    except Exception as e:
        address_book = AddressBook() if isinstance(AddressBook, type) else {}
        print(f"Помилка читання '{ADDRESSBOOK_FILE}': {e}. Створено порожню адресну книгу.")

    try:
        with open(NOTEBOOK_FILE, "r", encoding="utf-8") as f:
            nb_data = json.load(f)
        notebook = Notebook.from_dict(nb_data)
        notes_loaded = len(notebook._notes)
        print(f"Завантажено нотаток: {notes_loaded}")
    except FileNotFoundError:
        notebook = Notebook() if isinstance(Notebook, type) else {}
        print(f"Файл '{NOTEBOOK_FILE}' не знайдено. Створено порожній нотатник.")
    except JSONDecodeError as e:
        notebook = Notebook() if isinstance(Notebook, type) else {}
        print(f"Помилка читання '{NOTEBOOK_FILE}': некоректний JSON ({e}). Створено порожній нотатник.")
    except Exception as e:
        notebook = Notebook() if isinstance(Notebook, type) else {}
        print(f"Помилка читання '{NOTEBOOK_FILE}': {e}. Створено порожній нотатник.")

    return address_book, notebook

