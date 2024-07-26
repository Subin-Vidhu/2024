#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('office.db')

cursor = conn.execute("SELECT * FROM employees")
employees = list(cursor)

cursor = conn.execute("SELECT * FROM managers")
managers = list(cursor)

for employee in employees:
    print(employee)

#print(employees)
#print(managers)

conn.close()