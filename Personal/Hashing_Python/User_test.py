# pip install argon2-cffi
import argon2
from argon2 import PasswordHasher
import getpass
import json
import os

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the filename for the JSON file
FILENAME = os.path.join(SCRIPT_DIR, 'users.json')

def hash_password(password):
    """Hash a password using Argon2."""
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password

def verify_password(stored_password, provided_password):
    """Verify a password against a stored hashed password."""
    ph = PasswordHasher()
    try:
        ph.verify(stored_password, provided_password)
        return True
    except argon2.exceptions.VerificationError:
        print("Verification error")
        return False
    except argon2.exceptions.InvalidHash:
        print("Invalid hash")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def load_users():
    """Load users from the JSON file."""
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    """Save users to the JSON file."""
    with open(FILENAME, 'w') as f:
        json.dump(users, f)

def create_user(username, password):
    """Create a new user."""
    users = load_users()
    if username in users:
        print("Username already exists.")
        return False
    else:
        hashed_password = hash_password(password)
        users[username] = hashed_password
        save_users(users)
        return True

def login(username, password):
    """Login a user."""
    users = load_users()
    if username in users:
        stored_password = users[username]
        if verify_password(stored_password, password):
            return True
        else:
            return False
    else:
        return False

def main():
    while True:
        print("1. Create user")
        print("2. Login")
        print("3. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            if create_user(username, password):
                print("User created successfully.")
            else:
                print("Failed to create user.")
        elif choice == "2":
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            if login(username, password):
                print("Login successful.")
            else:
                print("Invalid username or password.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()