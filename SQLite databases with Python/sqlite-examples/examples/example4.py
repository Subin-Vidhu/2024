#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('coffee.db')

conn.execute("DELETE FROM USERS WHERE id=4")

cursor = conn.execute("SELECT * FROM USERS")
for row in cursor:
    print(row)

conn.close()