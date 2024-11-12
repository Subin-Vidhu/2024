Select all fields from the books table


SELECT *
FROM books;

Select unique authors from the books table

SELECT DISTINCT author
FROM books;

Select unique authors and genre combinations from the books table

SELECT DISTINCT author, genre
FROM books;

Aliasing
While the default column names in a SQL result set come from the fields they are created from, you've learned that aliasing can be used to rename these result set columns. This can be helpful for clarifying the intent or contents of the column.

Your task in this exercise is to incorporate an alias into one of the SQL queries that you worked with in the previous exercise!

Alias author so that it becomes unique_author
SELECT DISTINCT author AS unique_author
FROM books;

VIEWing your query
You've worked hard to create the below SQL query:

SELECT DISTINCT author AS unique_author
FROM books;
What if you'd like to be able to refer to it later, or allow others to access and use the results? The best way to do this is by creating a view. Recall that a view is a virtual table: it's very similar to a real table, but rather than the data itself being stored, the query code is stored for later use.

Save the results of this query as a view called library_authors
CREATE VIEW library_authors AS
SELECT DISTINCT author AS unique_author
FROM books;

-- Your code to create the view:
CREATE VIEW library_authors AS
SELECT DISTINCT author AS unique_author
FROM books;

-- Select all columns from library_authors
SELECT *
FROM library_authors;

-- Select the first 10 genres from books using PostgreSQL
SELECT genre
FROM books
LIMIT 10;

