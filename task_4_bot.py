import sys


def main():
    contacts = {}
    print("Hi! I'm your assistant bot")
    while True:
        run_bot(contacts)
    

def run_bot(contacts: dict):
    user_input = input("enter your command: ")
    hadle_input(user_input, contacts)


def hadle_input(input: str, contacts: dict):
    command, *args = parse_input(input)

    match command:
        case "hello":
            print("How can I help you?")
        case "add":
            print(add_contact(args, contacts))
        case "change":
            print(change_contact(args, contacts))
        case "phone":
            print(show_phone(args, contacts))
        case "all":
            print(show_all(contacts))
        case "exit" | "close": 
            print("Good bye!")
            sys.exit()
        case _:
            print("Invalid command. Try again.")


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            if func.__name__ == "add_contact" or func.__name__ == "change_contact":
                return "Give me name and phone please."
            elif func.__name__ == "show_phone":
                return "Enter user name please."
            else:
                return "Something went wrong."
        except IndexError:
            if func.__name__ == "show_phone":
                return "Enter user name please."
        except KeyError:
            if func.__name__ == "show_phone":
                return "You don't have such user in your contacts."

    return inner


@input_error
def add_contact(args, contacts: dict):   
    name, phone = args
    if name in contacts:
        confirmation = input(f"{name} already exist. Do you want to update it?")
        if confirmation.lower() != "yes":
            return f"{name} didn't change"
        
    contacts[name] = phone
    return "Contact added."
        

@input_error
def change_contact(args, contacts: dict):
    name, phone = args
    if name not in contacts:
        return f"No {name} in your contacts."
        
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts: dict):   
    name = args[0]  
    return f"{name}'s phone: {contacts[name]}"


def show_all(contacts: dict):
    if len(contacts) == 0:
        return "You don't have any contacts :("
    
    lines = []
    for name, phone in contacts.items():
        lines.append(f"{name}: {phone}")
    
    return "\n".join(lines)



if __name__ == "__main__":
    main()