### SQL Fundamentals - [Reference](https://www.w3resource.com/sql/tutorials.php#HISTSQL)

#### Schema SQL

```sql
CREATE TABLE User (
  id varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  lastName varchar(255) NOT NULL,
  dob date NOT NULL,
  sex varchar(1) NOT NULL,
  role varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO User
VALUES ('u1', 'George', 'Jacobson', '1992-01-01', 'm', 'manager');

INSERT INTO User
VALUES ('u2', 'Macy', 'Waterson', '1992-01-01', 'f', 'employee');

INSERT INTO User
VALUES ('u3', 'Bill', 'Peters', '1992-01-01', 'm', 'employee');


INSERT INTO User
VALUES ('u4','Janine', 'Wilson', '1992-01-01', 'f', 'manager');


INSERT INTO User
VALUES ('u5', 'Jason', 'Lipton', '1992-01-01', 'm', 'manager');
```

#### Query SQL

```sql
select * from User 
-- where role = 'employee';
```

### Imperative vs Declarative

- Imperative: How to do something, eg. Java
- Declarative: What to do, eg. SQL

### History of SQL

- 1970: SQL was developed at IBM by Donald D. Chamberlin and Raymond F. Boyce
- `Sequel`: Structured English Query Language
- For more information, check out the [video](https://youtu.be/KG-mqHoXOXY?si=ZQOvDpY2gS0W8dE7)

### SQL Standards

- SQL-86 (SQL-1)
- SQL-89 (SQL-2)
- SQL-92 (SQL-3)
- SQL:1999 (SQL-3)
- SQL:2003 (SQL-3)
- SQL:2008 (SQL-3)
- SQL:2011 (SQL-3)
- SQL:2016 (SQL-3)
- SQL:2019 (SQL-3)
- SQL:2023 (SQL-3)

- These are some of the SQL standards that have been released over the years and the latest one is SQL:2023.

### DATABASES

- A database is a collection of data stored in a computer system. Databases are organized in such a way that computer programs can easily access the data.

### Data Base Management System (DBMS)

- A DBMS is a software that allows a computer to perform database functions such as storing, retrieving, adding, deleting, and modifying data.

- Examples of DBMS include MySQL, PostgreSQL, SQLite, Oracle, SQL Server, and many more.

### Database Models

- Hierarchical Model: This model organizes data in a tree-like structure, with a single root, to which all the other data is linked. This model is not widely used today.

- Network Model: This model is an extension of the hierarchical model, where each child can have multiple parents. This model is also not widely used today.

- `Relational Model`: This model organizes data into tables, where each table has rows and columns. This model is the most widely used today. eg. MySQL, PostgreSQL, SQLite, Oracle, SQL Server, etc.

- Object-Oriented Model: This model organizes data into objects, which consist of attributes and methods. This model is used in object-oriented programming languages.

- Document Model: This model organizes data into documents, which can contain nested documents and arrays. This model is used in document-oriented databases.

- Graph Model: This model organizes data into nodes and edges, which represent entities and relationships. This model is used in graph databases.

- Entity-Relationship Model: This model organizes data into entities and relationships, which represent real-world entities and their relationships. This model is used in entity-relationship diagrams.

### TABLES

- A table is a collection of related data stored in rows and columns. Each row represents a record, and each column represents a field.

- A table is also known as a relation in the relational model.

- A table has a name, which is used to identify the table.

- A table has columns, which are used to define the fields of the table.

- A table has rows, which are used to store the records of the table.

- A table has a primary key, which is used to uniquely identify each row in the table.

### COLUMNS

- A column is a vertical arrangement of data in a table. Each column represents a field in the table.

- A column has a name, which is used to identify the column.

- A column has a data type, which defines the type of data that can be stored in the column.

- A column has a size, which defines the maximum length of the data that can be stored in the column.

- A column can have domain/constraints, which define the rules that the data in the column must follow.

- Columns are also known as attributes in the relational model.

### ROWS

- A row is a horizontal arrangement of data in a table. Each row represents a record in the table.

- A row has a primary key, which is used to uniquely identify the row in the table.

- A row has a value for each column in the table.

- A row is also known as a tuple in the relational model.

- A row is also known as a record in the database.

- Cardinality: The number of rows in a table is known as the cardinality of the table.

### PRIMARY KEY

- A primary key is a column or a set of columns that uniquely identifies each row in a table.

- A primary key must contain unique values.

- A primary key cannot contain NULL values.

- A primary key is used to enforce entity integrity.

- A primary key is also known as a candidate key in the relational model.

### FOREIGN KEY

- A foreign key is a column or a set of columns that references a primary key in another table.

- A foreign key is used to enforce referential integrity.

- A foreign key can contain NULL values.

- A foreign key is also known as a referencing key in the relational model.

### OLTP vs OLAP

- OLTP (Online Transaction Processing): OLTP systems are used to manage day-to-day transactions, such as sales, orders, and payments. OLTP systems are optimized for fast and efficient transaction processing.

- OLAP (Online Analytical Processing): OLAP systems are used to analyze and report on data, such as sales trends, customer behavior, and market share. OLAP systems are optimized for complex queries and data analysis.

### Popular SQL Databases

- MySQL: MySQL is an open-source relational database management system that is widely used for web applications.

- PostgreSQL: PostgreSQL is an open-source relational database management system that is known for its advanced features and extensibility.

- SQLite: SQLite is a lightweight relational database management system that is embedded in many applications.

- Oracle: Oracle is a commercial relational database management system that is widely used in enterprise applications.

- SQL Server: SQL Server is a commercial relational database management system that is developed by Microsoft.

### PostgreSQL

- PostgreSQL is an open-source relational database management system that is known for its advanced features and extensibility.

- PostgreSQL is widely used for web applications, data warehousing, and business intelligence.

- PostgreSQL supports a wide range of data types, including integers, floats, strings, dates, and arrays.

- PostgreSQL supports advanced features such as transactions, views, triggers, and stored procedures.

- PostgreSQL is known for its extensibility, with support for custom data types, custom functions, and custom indexes.

- PostgreSQL is known for its performance, with support for parallel query processing, query optimization, and indexing.

- PostgreSQL is known for its reliability, with support for high availability, replication, and backup and recovery.

- For this course, we will be using `PostgreSQL` as our database and `valentina studio`[To install](https://valentina-db.com/en/studio/download#:~:text=Valentina%20Studio%20Win%2064) as our database client.


    #### Assuming th employees.sql is the path in the cmd, and a DB called Employees is created, then the command to run the sql file is as follows:
    ```
    path: "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d Employees < employees.sql
    Password for user postgres:
    ```
    
### Queries in SQL

- A query is a request for data from a database. Queries are used to retrieve, insert, update, and delete data in a database.

- A query is written in SQL (Structured Query Language), which is a standard language for interacting with databases.

- A query consists of one or more SQL statements, which are used to perform operations on the database.

- A query can be simple or complex, depending on the requirements of the user.

- A query can be executed using a database client, such as `valentina studio`, `pgAdmin`, or `SQL Server Management Studio`.

 - ![alt text](image.png)
 