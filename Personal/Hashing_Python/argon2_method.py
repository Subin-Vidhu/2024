# argon2
import argon2
from argon2 import PasswordHasher
import getpass

def hash_password(password):
    ph = PasswordHasher()
    hashed_password = ph.hash(password)

    return hashed_password

def verify_password(stored_password, provided_password):
    ph = PasswordHasher()
    try:
        ph.verify(stored_password, provided_password)
        return True
    except:
        return False

def main():
    # Get the password from the user
    password = getpass.getpass("Enter your password: ")

    # Hash the password
    hashed_password = hash_password(password)

    print("Hashed Password: ", hashed_password)

    # Verify the password
    provided_password = getpass.getpass("Enter your password again: ")
    if verify_password(hashed_password, provided_password):
        print("Password is correct")
    else:
        print("Password is incorrect")

if __name__ == "__main__":
    main()