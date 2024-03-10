
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self._validate_phone():
            raise ValueError("Invalid phone number format")

    def _validate_phone(self):
        return len(self.value) == 10 and self.value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f', birthday: {self.birthday}' if self.birthday else ''
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                if (next_birthday - today).days <= 7:
                    upcoming_birthdays.append((record.name.value, next_birthday))
        return upcoming_birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            if isinstance(e, KeyError):
                return "Enter user name."
            elif isinstance(e, ValueError):
                return "Give me name and phone with 10 chapters please."
            elif isinstance(e, IndexError):
                return "Invalid number of arguments."
    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_user_phone(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.edit_phone(record.phones[0].value, phone)
    return "Contact changed."

@input_error
def phone_username(name, book: AddressBook):
    record = book.find(name)
    if record:
        return f"Phone number for contact '{name}': {record.phones[0]}"
    else:
        raise KeyError("Contact not found.")

@input_error
def all_users_phone(book: AddressBook):
    return '\n'.join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday for contact '{name}': {record.birthday}"
    else:
        raise KeyError("Contact not found or birthday not set.")

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return '\n'.join([f"{name}: {birthday.strftime('%d.%m.%Y')}" for name, birthday in upcoming_birthdays])
    else:
        return "No upcoming birthdays."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_user_phone(args, book))

        elif command == "phone":
            print(phone_username(args[0], book))

        elif command == "all":
            print(all_users_phone(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()