# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 08:30:03 2024

@author: Subin-PC
"""

#bcrypt
import bcrypt
import getpass

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def verify_password(stored_password, provided_password):
    # Check if the provided password matches the stored password
    if bcrypt.checkpw(provided_password.encode('utf-8'), stored_password):
        return True
    else:
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