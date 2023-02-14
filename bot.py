import functools
import re
from collections import OrderedDict
from typing import Callable


def add(*args: str) -> str:
    if contacts.get(args[0]):
        return 'Sorry, this contact already exists'
    contacts.update({args[0]:args[1]})
    return 'Done!'

def change(*args: str) -> str:
    if not contacts.get(args[0]):
        raise KeyError
    contacts[args[0]] = args[1]
    return 'Done!'

def decorator_input(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*words):
        try:
            return func(*words)
        except KeyError:
            return "This user doesn't exist"
        except IndexError:
            return "You didn't enter the name or the phone."
        except TypeError:
            return "Sorry, this command doesn't exist"
    return wrapper

def get_command(command: str) -> Callable:
    words = command.split(' ')
    for key in COMMANDS_DICT.keys():
        if re.search(fr'\b{words[0].lower()}\b', str(key)):
            func = COMMANDS_DICT[key]
            return func

def get_contacts() -> dict:
    with open('contacts.txt', 'a+') as fh:
        fh.seek(0)
        text = fh.readlines()

    contacts = {}
    
    for line in text:
        words = line.split(': ')
        contacts.update({words[0]:words[1].rstrip('\n')})
    
    return contacts

def goodbye() -> str:
    return 'Goodbye!'

def hello() -> str:
    return 'How can I help you?'

def phone(*args: str) -> str:
    if not contacts.get(args[0]):
        raise KeyError
    return contacts[args[0]]

def showall() -> dict[str,str]:
    return contacts
    
def write_contacts() -> None:
    text = []
    contacts_ord = OrderedDict(sorted(contacts.items()))
    for name, number in contacts_ord.items():
        text.append(f'{name}: {number}\n')
    with open('contacts.txt', 'w') as fh:
        fh.write(''.join(text))


COMMANDS_DICT = {('hello','hi'):hello,
                 'add':add,
                 'change':change,
                 'phone':phone,
                 'showall':showall,
                 ('goodbye','close','exit','quit'):goodbye
}

def main():

    global contacts
    contacts = get_contacts()

    while True:

        command = input(">>> ")
        words = command.split(' ')
        func = get_command(command)
        func = decorator_input(func)
        print(func(*words[1:])) 
        if func.__name__ == 'goodbye':
            write_contacts()
            break

if __name__ == '__main__':
    main()
   