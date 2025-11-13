from decorators import input_error
from entities import AddressBook, Record


@input_error
def add_contact(args: list[str], contacts: AddressBook) -> str:
    """Add a new contact or phone to existing contact"""
    if len(args) < 2:
        raise ValueError("Not enough arguments. Usage: add [name] [phone]")
    
    contact_name, contact_phone_number = args[0], args[1]
    record = contacts.find(contact_name)
    if record is None:
        record = Record(contact_name)
        contacts.add_record(record)

    record.add_phone(contact_phone_number)
    return f"✅ Contact {contact_name} added successfully"


@input_error
def get_phone(args: list[str], contacts: AddressBook) -> str:
    """Show all phones of a contact"""
    if len(args) < 1:
        raise ValueError("Not enough arguments. Usage: phone [name]")
    
    contact_name = args[0]
    record = contacts.find(contact_name)
    
    if record is None:
        raise KeyError(f"❌ Contact {contact_name} not found")
    
    if not record.phones:
        return f"📭 Contact {contact_name} has no phones"
    
    phones_str = ', '.join(phone.value for phone in record.phones)
    plural = "s" if len(record.phones) > 1 else ""
    return f"📞 Contact {contact_name} phone number{plural}: {phones_str}"


@input_error
def get_all(_: list[str], contacts: AddressBook) -> str:
    """Show all contacts with full information"""
    result: list[str] = []

    if not contacts.data:
        return "📭 No contacts found"

    for contact_name, record in contacts.data.items():
        # Phones
        phones_str = ', '.join(phone.value for phone in record.phones) if record.phones else "no phones"
        
        # Birthday
        birthday_str = f" - Birthday: {record.birthday.value.strftime('%d.%m.%Y')}" if record.birthday and record.birthday.value else ""
        
        # Email
        email_str = f" - Email: {record.email.value}" if record.email and record.email.value else ""
        
        # Address
        address_str = f" - Address: {record.address.value}" if record.address and record.address.value else ""
        
        result.append(f"👤 {contact_name} - {phones_str}{birthday_str}{email_str}{address_str}")

    return "\n".join(result)


@input_error
def search_contacts(args: list, contacts: AddressBook) -> str:  
    """Search contacts by name or phone number"""
    if len(args) < 1:
        raise ValueError("Not enough arguments. Usage: search [query]")
    
    query = args[0]
    results = contacts.search(query)  
    
    if not results:
        return f"🔍 Nothing found for query '{query}'"
    
    result_lines = [f"🔍 Found contacts: {len(results)}"]
    
    for record in results:
        phones = [phone.value for phone in record.phones]
        phones_str = ', '.join(phones) if phones else "no phones"
        result_lines.append(f"👤 {record.name.value}: {phones_str}")
    
    return "\n".join(result_lines)


@input_error
def change_phone(args: list[str], contacts: AddressBook) -> str:
    """Change phone number of existing contact"""
    if len(args) < 3:
        raise ValueError("Not enough arguments. Usage: change [name] [old_phone] [new_phone]")
    
    contact_name, old_phone_number, new_phone_number = args[0], args[1], args[2]
    record = contacts.find(contact_name)
    
    if record is None:
        raise KeyError(f"❌ Contact {contact_name} not found")
    
    if record.edit_phone(old_phone_number, new_phone_number):
        return f"✅ Contact {contact_name} updated successfully"
    else:
        raise ValueError(f"Phone {old_phone_number} not found for contact {contact_name}")


@input_error
def delete_contact(args: list, contacts: AddressBook) -> str:  
    """Delete a contact by name"""
    if len(args) < 1:
        raise ValueError("Not enough arguments. Usage: delete [name]")
    
    name = args[0]
    record = contacts.find(name)  
    
    if record is None:
        raise KeyError(f"❌ Contact {name} not found")
    
    contacts.delete(name)  
    return f"✅ Contact {name} deleted"


@input_error
def add_email(args: list, contacts: AddressBook) -> str:  
    """Add email to existing contact"""
    if len(args) < 2:
        raise ValueError("Not enough arguments. Usage: add-email [name] [email]")
    
    name, email = args[0], args[1]
    record = contacts.find(name)  
    
    if record is None:
        raise KeyError(f"❌ Contact {name} not found")
    
    record.add_email(email)
    return f"✅ Email added to contact {name}"


@input_error
def add_address(args: list, contacts: AddressBook) -> str:  
    """Add address to existing contact"""
    if len(args) < 2:
        raise ValueError("Not enough arguments. Usage: add-address [name] [address...]")
    
    name = args[0]
    address = " ".join(args[1:])
    record = contacts.find(name)  
    
    if record is None:
        raise KeyError(f"❌ Contact {name} not found")
    
    record.add_address(address)
    return f"✅ Address added to contact {name}"


handlers: dict[str, callable] = {
    "add": add_contact,
    "phone": get_phone,
    "all": get_all,
    "search": search_contacts,
    "change": change_phone,
    "delete": delete_contact,
    "add-email": add_email,
    "add-address": add_address,
}