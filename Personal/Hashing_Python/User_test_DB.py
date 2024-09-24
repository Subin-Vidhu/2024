import argon2
from argon2 import PasswordHasher
import mysql.connector
import getpass

# Create a connection to the MySQL database
def create_connection():
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='password',
            host='127.0.0.1'
        )
        return cnx
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return None

# Create a cursor object
def create_cursor(cnx):
    try:
        cursor = cnx.cursor()
        return cursor
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return None

# Create a new database
def create_database(cursor, database_name):
    query = "CREATE DATABASE {}".format(database_name)
    try:
        cursor.execute(query)
        print("Database created successfully.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

# Create a new table
def create_table(cursor, database_name, table_name):
    query = "USE {}".format(database_name)
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    query = "CREATE TABLE {} (id INT AUTO_INCREMENT, username VARCHAR(255), password VARCHAR(255), PRIMARY KEY (id))".format(table_name)
    try:
        cursor.execute(query)
        print("Table created successfully.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

# Check if database exists
def check_database_exists(cursor, database_name):
    query = "SHOW DATABASES LIKE '{}'".format(database_name)
    try:
        cursor.execute(query)
        if cursor.fetchone():
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False

# Check if table exists
def check_table_exists(cursor, database_name, table_name):
    query = "USE {}".format(database_name)
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    query = "SHOW TABLES LIKE '{}'".format(table_name)
    try:
        cursor.execute(query)
        if cursor.fetchone():
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False

# Create a new user
def create_user(cursor, database_name, username, password):
    query = "USE {}".format(database_name)
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        cursor.execute(query, (username, hashed_password))
        print("User created successfully.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

# Verify a user's password
def verify_password(cursor, database_name, username, password):
    query = "USE {}".format(database_name)
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    query = "SELECT password FROM users WHERE username = %s"
    try:
        cursor.execute(query, (username,))
        stored_password = cursor.fetchone()[0]
        ph = PasswordHasher()
        try:
            ph.verify(stored_password, password)
            return True
        except argon2.exceptions.VerificationError:
            return False
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False

def main():
    cnx = create_connection()
    if cnx is not None:
        cursor = create_cursor(cnx)
        if cursor is not None:
            database_name = "test_hashing"
            table_name = "users"
            if not check_database_exists(cursor, database_name):
                create_database(cursor, database_name)
            if not check_table_exists(cursor, database_name, table_name):
                create_table(cursor, database_name, table_name)
            while True:
                print("1. Create user")
                print("2. Login")
                print("3. Quit")
                choice = input("Choose an option: ")
                if choice == "1":
                    username = input("Enter your username: ")
                    password = getpass.getpass("Enter your password: ")
                    create_user(cursor, database_name, username, password)
                elif choice == "2":
                    username = input("Enter your username: ")
                    password = getpass.getpass("Enter your password: ")
                    if verify_password(cursor, database_name, username, password):
                        print("Login successful.")
                    else:
                        print("Invalid username or password.")
                elif choice == "3":
                    break
                else:
                    print("Invalid choice. Please choose again.")
        else:
            print("Failed to create cursor.")
    else:
        print("Failed to connect to database.")

if __name__ == "__main__":
    main()