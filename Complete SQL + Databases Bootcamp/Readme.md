### SQL Fundamentals

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



