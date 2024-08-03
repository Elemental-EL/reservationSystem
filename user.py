import json
import os
import re
import bcrypt


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
        print(f"{field_name} cannot be empty.")
        return False
    return True


def sign_up():
    """Creates a new user."""
    username = input("Enter username: ")
    if not validate_input("Username", username):
        sign_up()
    users = load_users()
    if username in users:
        print("Username already exists. Please choose another one.")
        sign_up()
    password = input("Enter password: ")
    if not validate_input("Password", password) or not is_valid_password(password):
        print("Password must be between 8 and 32 characters and contain at least one letter and one number.")
        sign_up()
    first_name = input("Enter first name: ")
    if not validate_input("First name", first_name):
        sign_up()
    last_name = input("Enter last name: ")
    if not validate_input("Last name", last_name):
        sign_up()
    user = User(username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), first_name,
                last_name)
    users[username] = user.to_dict()
    save_users(users)
    print("Sign up successful!")
    return username


def log_in():
    """If the credentials are valid, logs in the user."""
    username = input("Enter username: ")
    password = input("Enter password: ")

    users = load_users()
    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]['password'].encode('utf-8')):
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None
