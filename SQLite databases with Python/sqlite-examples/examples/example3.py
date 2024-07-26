#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('coffee.db')

conn.execute("UPDATE USERS SET name='Tamara' WHERE id=1")

cursor = conn.execute("SELECT * FROM USERS")
for row in cursor:
    print(row)

conn.close()