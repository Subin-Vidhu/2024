#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('coffee.db')

print("Opened database")

conn.execute('''CREATE TABLE USERS
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL);''')

print("Table created successfully")

conn.execute("INSERT INTO USERS (ID,NAME) VALUES (1, 'Paul')");
conn.execute("INSERT INTO USERS (ID,NAME) VALUES (2, 'Alice')");
conn.execute("INSERT INTO USERS (ID,NAME) VALUES (3, 'Bob')");
conn.execute("INSERT INTO USERS (ID,NAME) VALUES (4, 'Lauren')");

conn.commit()


conn.close()