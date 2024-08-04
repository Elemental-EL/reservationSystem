import json
import os
import re
import bcrypt
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console(color_system="windows")


class User:
    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name
        }


def load_users():
    """Loads the information of the users."""
    if not os.path.exists('users.json'):
        return {}
    with open('users.json', 'r') as file:
        return json.load(file)


def save_users(users):
    """Saves the information of the users with the changes made to them."""
    with open('users.json', 'w') as file:
        json.dump(users, file)


def is_valid_password(password):
    """Checks if the password is valid."""
    return 8 <= len(password) <= 32 and re.search(r'\d', password) and re.search(r'[A-Za-z]', password)


def validate_input(field_name, value):
    """Checks if the input is not empty."""
    if not value.strip():
        console.print(f"[red]{field_name} cannot be empty.[/red]")
        return False
    return True


def sign_up():
    """Creates a new user."""
    console.print("[bold blue]Sign Up[/bold blue]")
    while True:
        username = Prompt.ask("Enter username")
        if not validate_input("Username", username):
            continue
        users = load_users()
        if username in users:
            console.print("[red]Username already exists. Please choose another one.[/red]")
            continue

        password = Prompt.ask("Enter password")
        if not validate_input("Password", password) or not is_valid_password(password):
            console.print("[red]Password must be between 8 and 32 characters and contain at least one letter and one "
                          "number.[/red]")
            continue

        first_name = Prompt.ask("Enter first name")
        if not validate_input("First name", first_name):
            continue

        last_name = Prompt.ask("Enter last name")
        if not validate_input("Last name", last_name):
            continue

        user = User(username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), first_name,
                    last_name)
        users[username] = user.to_dict()
        save_users(users)
        console.print("[bold green]Sign up successful![/bold green]")
        return username


def log_in():
    """If the credentials are valid, logs in the user."""
    console.print("[bold blue]Log In[/bold blue]")
    while True:
        username = Prompt.ask("Enter username")
        password = Prompt.ask("Enter password")

        users = load_users()
        if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]['password'].encode('utf-8')):
            console.print("[bold green]Login successful![/bold green]")
            return username
        else:
            console.print("[red]Invalid username or password.[/red]")
            retry = Confirm.ask("Do you want to try again?")
            if not retry:
                return None
