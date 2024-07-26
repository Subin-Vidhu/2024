### SQLite databases with Python

# Database Basics

## Table of Contents

* [What is SQLite?](#what-is-sqlite)
* [What is SQL?](#what-is-sql)
* [How does Python interact with SQLite?](#how-does-python-interact-with-sqlite)
* [Database Structure](#database-structure)
* [SQLite File Structure](#sqlite-file-structure)
* [SQLite Browser](#sqlite-browser)
* [Basic Database Operations](#basic-database-operations)
* [Example SQL Queries](#example-sql-queries)

## What is SQLite?

SQLite is a self-contained, file-based database system that allows you to store and manage data in a structured format.

## What is SQL?

SQL (Structured Query Language) is a programming language used to interact with databases. It allows you to create, modify, and query data in a database.

## How does Python interact with SQLite?

Python can use SQLite to store and manage data. Python provides a built-in module called `sqlite3` that allows you to interact with SQLite databases.

## Database Structure

Data is stored in tables, which are similar to spreadsheets. Each table has rows and columns, where each row represents a single record and each column represents a field or attribute of that record.

## SQLite File Structure

SQLite stores the entire database (all tables) in a single file. This file can be easily shared or moved between different systems.

## SQLite Browser

SQLite Browser is a free, open-source tool that allows you to design and edit SQLite databases. It provides a graphical interface for creating and modifying tables, as well as executing SQL queries.

## Basic Database Operations

The basic operations in a database are:

* **Create**: Create a new table or insert new data into an existing table.
* **Read**: Retrieve data from a table.
* **Update**: Modify existing data in a table.
* **Delete**: Delete data from a table.

## Example SQL Queries

### Create a Table

Create a table named `users` with columns `id` and `name`:
```sql
CREATE TABLE USERS
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL);
```
Read Data from a Table
Read data from the users table:
```sql
SELECT * FROM USERS
```
Update Data in a Table
Update the name of the user with id 1:
```sql
UPDATE USERS SET NAME = 'John' WHERE ID = 1
```
Delete Data from a Table
Delete the user with id 1:
```sql
DELETE FROM USERS WHERE ID = 1
```
These are just a few examples of SQL queries that you can use to interact with SQLite databases in Python.

For more information on SQLite and the `sqlite3` module in Python, refer to the official documentation:
* [SQLite Documentation](https://www.sqlite.org/docs.html)
         