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

- Imperative: How to do something
- Declarative: What to do


