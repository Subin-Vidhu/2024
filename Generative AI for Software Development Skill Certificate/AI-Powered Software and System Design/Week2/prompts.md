- Design and Implement a Database Schema with an LLM

    - Instruction 1:

        Try prompting an LLM to create a database schema using the same prompt as Laurence: 

        Design a database schema for an e-commerce application with tables for users, products, orders, and order_items.

        Then modify the prompt to see how the schema changes. Try specifying attribute names, or allowed datatypes for columns, and see how the LLM updates its proposed schema. 

    - Instruction 2:

        Work with an LLM to create tables for your database using the schema outlined in the ecommerce_schema.txt file in the video downloads.

        Be sure to provide the LLM details about your database setup.

    - Instruction 3:

        The code from the slides is available in the database_with_tables.py file

- Implementing CRUD operations with an LLM

    - Instruction 1:

        You’ll get the most from this video if you follow along and pair-code with an LLM!

        You can use your own code from the previous video, or the database code in the database_with_tables.py file in the downloads for this video, to prompt your LLM as you follow what Laurence is doing.

        You can also try out the code your LLM writes for you using the Database_with_tables.ipynb notebook file - just be sure to have SQLAlchemy installed!

    - Instruction 2:

        Take a moment to implement CREATE functionality for your database, and then add a new user named ‘John Doe’ with email ‘john.doe@example.com’.

    - Instruction 3:

        Prompt an LLM to create READ functionality for your database. 

        Then implement the code in your database and check that it returns the John Doe user you added earlier.

    - Instruction 4:

        Take a moment to prompt an LLM to implement code to update the database. The code should allow you to modify a user record.

        Then implement the code in your database and check that you can update the email of the user John Doe to “john.new@example.com”.

    - Instruction 5:

        Prompt an LLM to implement code to delete a record from the database. 

        Then implement the code in your database and check that you can delete the user John Doe. Use your read function to check that the user has been deleted.

- Debugging

    Prompt the LLM to tell you how to use the EXPLAIN feature in SQLAlchemy to debug queries, and ask it to add code to your database to implement this.Prompt the LLM to tell you how to use the EXPLAIN feature in SQLAlchemy to debug queries, and ask it to add code to your database to implement this.