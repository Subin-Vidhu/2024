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




