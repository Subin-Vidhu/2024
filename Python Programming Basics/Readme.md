### Introduction

 - Python's popularity stems from its simplicity, versatility, and robustness.

   - Readable and Simple Syntax
   - Extensive Standard Library
   - Dynamic Typing and Dynamic Binding
   - Cross-platform Compatibility
   - High-level Language
   - Support for Multiple Programming Paradigms
   - Large and Active Community
   - Scalability and Performance
   - Open Source and Free

- Python is an interpreted language, which means that it is executed line by line. This makes it easier to debug and test code.

- Python is a high-level language, which means that it is closer to human language than machine language. This makes it easier to write and read code.

- Python is a dynamically typed language, which means that you don't have to declare the type of a variable when you create it. This makes it easier to write code quickly.

### Python Installation

- Python can be installed on Windows, macOS, and Linux.

- To install Python on Windows, follow these steps:

  - Download the latest version of Python from the official website.
  - Run the installer.
  - Check the box that says "Add Python to PATH".
  - Click "Install Now".
  - Wait for the installation to finish.
  - Click "Close".

### Hello World

- To print "Hello, World!" in Python, use the following code: 

  - Open a terminal or command prompt.
 Type `python` to open the Python interpreter.
  Type the following code:


    ```python
    print("Hello, World!")
    ```

- To run the code, save it in a file with a `.py` extension and run it using the Python interpreter. how?
  
    - Open a terminal or command prompt.
    - Navigate to the directory where the file is saved.
    - Run the following command:
  
      ```bash
      python filename.py
      ```

- You can also run the code in an interactive Python shell.
   
### Comments

Single-line comments in Python start with a hash symbol `#`. They are used to explain the code and make it more readable.

```python
# This is a single-line comment

print("Hello, World!") # This is another single-line comment
```

Multi-line comments in Python are created using triple quotes `"""` or `'''`.

```python
"""
This is a multi-line comment.
It can span multiple lines.
"""

'''
This is another multi-line comment.
It can also span multiple lines.
'''
```

### Variables

- Variables are used to store data in a program. They are created using an assignment operator `=`.

- Variable names can contain letters, numbers, and underscores. They cannot start with a number.

- Python is a dynamically typed language, which means that you don't have to declare the type of a variable when you create it.

- To create a variable in Python, use the following syntax:

  ```python
  variable_name = value
  ```

- To access the value of a variable, use the variable name.

- Variables can be of different types, such as integers, floats, strings, lists, tuples, dictionaries, etc.

- To check the type of a variable, use the `type()` function.

- To print the value of a variable, use the `print()` function.

- Constants are variables whose values do not change during the execution of a program. They are usually named using `uppercase` letters.

- If you want to prevent accidental modification of a constant value, you can use the readonly module to create immutable variables. Here's how you can do it:

  ```python
  from readonly import readonly

  @readonly
  CONSTANT_NAME = value
  ```

 - Multiple assignments can be done in a single line using the following syntax:

      ```python
      a = b = c = value
      ```

    - Tuple unpacking can be used to assign multiple values to multiple variables in a single line:

      ```python
      a, b, c = value1, value2, value3
      ```
      
    - You can swap the values of two variables using the following syntax:
      
        ```python
        a, b = b, a
        ```

    - List unpacking can be used to assign multiple values to multiple variables in a single line:

      ```python
      [a, b, c] = [value1, value2, value3]
      ```

    - Extended unpacking can be used to assign multiple values to multiple variables in a single line:

      ```python
      a, *b, c = value1, value2, value3, value4
      ```

       - example:

          ```python
          a, *b, c = 1, 2, 3, 4, 5
          print(a) # prints 1
          print(b) # prints [2, 3, 4]
          print(c) # prints 5
          ```

  - You can use the `global` keyword to access a global variable inside a function.

- Variable scope refers to the visibility of a variable within a program.

- You can delete a variable using the `del` keyword.

- You can check if a variable is defined using the `defined()` function.


### Data Types

- Python has several built-in data types, such as integers, floats, strings, lists, tuples, dictionaries, etc.

- Integers are whole numbers, such as `1`, `2`, `3`, etc.

- Floats are numbers with a decimal point, such as `1.0`, `2.5`, `3.14`, etc.

- Strings are sequences of characters, such as `"Hello"`, `"World"`, `"Python"`, etc.

  - You can use single quotes `'` or double quotes `"` to create strings.

  - You can use triple quotes `'''` or `"""` to create multi-line strings.

  - You can concatenate strings using the `+` operator.

  - You can repeat strings using the `*` operator.

  - You can access individual characters in a string using indexing.

  - You can slice strings to get a substring.

  - Strings are immutable, which means that you cannot change the value of a string once it is created.

  - You can convert a string to uppercase or lowercase using the `upper()` and `lower()` methods.

  - You can remove whitespace from the beginning and end of a string using the `strip()` method.

  - You can split a string into a list of substrings using the `split()` method.

  - You can join a list of strings into a single string using the `join()` method.

  - You can format strings using the `format()` method.

  - You can check if a string contains a substring using the `in` operator.

  - You can compare strings using comparison operators, such as `==`, `!=`, `<`, `>`, `<=`, and `>=`.

  - You can get the length of a string using the `len()` function.

  - You can convert a string to an integer or float using the `int()` and `float()` functions.

  - You can check if a string is numeric using the `isnumeric()` method.

  - You can check if a string is alphabetic using the `isalpha()` method.

  - You can check if a string is alphanumeric using the `isalnum()` method.

  - You can check if a string is in title case using the `istitle()` method.

  - You can check if a string is in uppercase using the `isupper()` method.

  - You can check if a string is in lowercase using the `islower()` method.

  - You can check if a string starts with a substring using the `startswith()` method.

  - You can check if a string ends with a substring using the `endswith()` method.

  - You can replace substrings in a string using the `replace()` method.

  - You can find the index of a substring in a string using the `find()` method.

  - You can count the occurrences of a substring in a string using the `count()` method.

  - You can check if a string is empty using the `bool()` function.

  - You can check if a string is a valid identifier using the `isidentifier()` method.

  - You can check if a string is a valid number using the `isnumeric()`, `isdecimal()`, `isdigit()`, `isdecimal

  - f-strings are a new way to format strings in Python 3.6 and later. They are prefixed with an `f` or `F` and contain expressions inside curly braces `{}`.

    - example:

        ```python
        name = "Alice"
        age = 30
        print(f"My name is {name} and I am {age} years old.")
        ```
   - Escape characters are used to include special characters in strings, such as newline `\n`, tab `\t`, backslash `\\`, etc.

     - example:

        ```python
        print("Hello\nWorld") # prints Hello on one line and World on the next line
        print("Hello\tWorld") # prints Hello and World separated by a tab
        print("Hello\\World")   # prints Hello\World
        print("Hello\rWorld") # prints World on top of Hello - carriage return. It moves the cursor to the beginning of the line. It is used to overwrite the text. More examples:

        print("Hello\bWorld") # prints HelWorld - backspace. It moves the cursor one character back. It is used to delete the character before the cursor. More examples:

        print("Hello\fWorld") # prints HelloWorld - form feed. It moves the cursor to the next page. It is used to separate the text. More examples:

        print("Hello\vWorld") # prints HelloWorld - vertical tab. It moves the cursor to the next line. It is used to separate the text. More examples:

        print("Hello\aWorld") # prints HelloWorld - alert. It produces a sound. More examples:


        ```
  

- Lists are ordered collections of items, such as `[1, 2, 3]`, `["a", "b", "c"]`, etc.

   - You can access individual items in a list using indexing.

    - You can slice lists to get a sublist.

    - Lists are mutable, which means that you can change the value of an item in a list.

    - You can add items to a list using the `append()` method.

       - example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits.append("orange")
          print(fruits) # prints ["apple", "banana", "cherry", "orange"]
          ```

    - You can insert items into a list at a specific position using the `insert()` method.

      - example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits.insert(1, "orange")
          print(fruits) # prints ["apple", "orange", "banana", "cherry"]
          ```

    - You can remove items from a list using the `remove()` method.
      
        - example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            fruits.remove("banana")
            print(fruits) # prints ["apple", "cherry"]
            ```

    - You can remove items from a list by index using the `pop()` method.
      
        - example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            fruits.pop(1)
            print(fruits) # prints ["apple", "cherry"]
            ```

    - You can remove items from a list by value using the `del` keyword.
      
        - example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            del fruits[1]
            print(fruits) # prints ["apple", "cherry"]
            ```

    - You can clear a list using the `clear()` method.
        
        - example:
    
            ```python
              fruits = ["apple", "banana", "cherry"]
              fruits.clear()
              print(fruits) # prints []
              ```

    - You can copy a list using the `copy()` method.

      - example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits_copy = fruits.copy()
          print(fruits_copy) # prints ["apple", "banana", "cherry"]
          ```

    - You can join two lists using the `extend()` method.
      
        - example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            more_fruits = ["orange", "mango", "grape"]
            fruits.extend(more_fruits)
            print(fruits) # prints ["apple", "banana", "cherry", "orange", "mango", "grape"]
            ```

    - You can reverse a list using the `reverse()` method.
        
          - example:
    
              ```python
              fruits = ["apple", "banana", "cherry"]
              fruits.reverse()
              print(fruits) # prints ["cherry", "banana", "apple"]
              ```
    - You can sort a list using the `sort()` method.

      - example:

          ```python
          fruits = ["banana", "apple", "cherry"]
          fruits.sort()
          print(fruits) # prints ["apple", "banana", "cherry"]
          ```
    - You can count the occurrences of an item in a list using the `count()` method.
    
      - example:

          ```python
          fruits = ["apple", "banana", "cherry", "apple"]
          count = fruits.count("apple")
          print(count) # prints 2
          ```
    - You can get the index of an item in a list using the `index()` method.
      
        - example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            index = fruits.index("banana")
            print(index) # prints 1
            ``` 

    - You can check if an item is in a list using the `in` operator.

      - example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          if "banana" in fruits:
              print("Yes")
          else:
              print("No")
          ``` 

    - You can check if a list is empty using the `bool()` function.

      - example:

          ```python
          fruits = []
          if fruits:
              print("Yes")
          else:
              print("No")
          ```
    - You can convert a list to a string using the `join()` method.

      - example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits_str = ", ".join(fruits)
          print(fruits_str) # prints "apple, banana, cherry"
          ```
    - You can convert a string to a list using the `split()` method.

      - example:

          ```python
          fruits_str = "apple, banana, cherry"
          fruits = fruits_str.split(", ")
          print(fruits) # prints ["apple", "banana", "cherry"]
          ```
    - You can create a list using a list comprehension.
      
        - example:
  
            ```python
            numbers = [1, 2, 3, 4, 5]
            squares = [x**2 for x in numbers]
            print(squares) # prints [1, 4, 9, 16, 25]
            ```
    - You can create a list using the `range()` function.
      
        - example:
  
            ```python
            numbers = list(range(1, 6))
            print(numbers) # prints [1, 2, 3, 4, 5]
            ``` 

    - You can create a list using the `list()` function.

      - example:

          ```python
          numbers = list((1, 2, 3, 4, 5))
          print(numbers) # prints [1, 2, 3, 4, 5]
          ```

    - You can create a list using the `*` operator.

      - example:

          ```python
          numbers = [1, 2, 3] * 3
          print(numbers) # prints [1, 2, 3, 1, 2, 3, 1, 2, 3]
          ```
    - You can create a list using the `append()` method.
      
        - example:
  
            ```python
            numbers = []
            numbers.append(1)
            numbers.append(2)
            numbers.append(3)
            print(numbers) # prints [1, 2, 3]
            ``` 

    - You can create a list using the `insert()` method.

      - example:

          ```python
          numbers = [1, 3]
          numbers.insert(1, 2)
          print(numbers) # prints [1, 2, 3]
          ```
    - You can create a list using the `remove()` method.

      - example:

          ```python
          numbers = [1, 2, 3]
          numbers.remove(2)
          print(numbers) # prints [1, 3]
          ```
    - You can create a list using the `pop()` method.

      - example:

          ```python
          numbers = [1, 2, 3]
          numbers.pop()
          print(numbers) # prints [1, 2]
          ``` 

    - You can create a list using the `del` keyword.
      
        - example:
  
            ```python
            numbers = [1, 2, 3]
            del numbers[1]
            print(numbers) # prints [1, 3]
            ```
    - You can create a list using the `clear()` method.

      - example:

          ```python
          numbers = [1, 2, 3]
          numbers.clear()
          print(numbers) # prints []
          ``` 

    - You can create a list using the `copy()` method.

      - example:

          ```python
          numbers = [1, 2, 3]
          numbers_copy = numbers.copy()
          print(numbers_copy) # prints [1, 2, 3]
          ``` 

    - You can create a list using the `extend()` method.

      - example:

          ```python
          numbers = [1, 2, 3]
          more_numbers = [4, 5, 6]
          numbers.extend(more_numbers)
          print(numbers) # prints [1, 2, 3, 4, 5, 6]
          ```

    - You can create a list using the `reverse()` method.

      - example:

          ```python
          numbers = [1, 2, 3]
          numbers.reverse()
          print(numbers) # prints [3, 2, 1]
          ``` 

    - You can create a list using the `sort()` method.


      - example:

          ```python
          numbers = [3, 1, 2]
          numbers.sort()
          print(numbers) # prints [1, 2, 3]
          ```
    - sort vs sorted

      - The `sort()` method sorts the list in place, which means that it modifies the original list.

        - example:

            ```python
            numbers = [3, 1, 2]
            numbers.sort()
            print(numbers) # prints [1, 2, 3]
            ```

      - The `sorted()` function returns a new sorted list without modifying the original list.

        - example:

            ```python
            numbers = [3, 1, 2]
            sorted_numbers = sorted(numbers)
            print(numbers) # prints [3, 1, 2]
            print(sorted_numbers) # prints [1, 2, 3]
            ```


- Tuples are ordered collections of items that cannot be modified, such as `(1, 2, 3)`, `("a", "b", "c")`, etc.

    - You can access individual items in a tuple using indexing.

    - You can slice tuples to get a subtuple.

    - Tuples are immutable, which means that you cannot change the value of an item in a tuple.

    - You can convert a tuple to a list using the `list()` function.

    - You can convert a list to a tuple using the `tuple()` function.

    - You can create a tuple using the `*` operator.

    - You can create a tuple using the `+` operator.

    - You can create a tuple using the `count()` method.

    - You can create a tuple using the `index()` method.

    - You can create a tuple using the `in` operator.

    - You can create a tuple using the `len()` function.

    - You can create a tuple using the `sorted()` function.

    - You can create a tuple using the `sum()` function.

    - You can create a tuple using the `max()` function.

    - You can create a tuple using the `min()` function.

    - tuple to string using the `join()` method.
       - example:

          ```python
          fruits = ("apple", "banana", "cherry")
          fruits_str = ", ".join(fruits)
          print(fruits_str) # prints "apple, banana, cherry"
          ```
    - string to tuple using the `split()` method.
      
        - example:
  
            ```python
            fruits_str = "apple, banana, cherry"
            fruits = tuple(fruits_str.split(", "))
            print(fruits) # prints ("apple", "banana", "cherry")
            ```

- Dictionaries are unordered collections of key-value pairs, such as `{"name": "Alice", "age": 30}`, `{"a": 1, "b": 2}`, etc.

  - You can access the value of a key in a dictionary using indexing.

    - example: 

        ```python
        person = {"name": "Alice", "age": 30}
        name = person["name"]
        print(name) # prints "Alice"
        ```

  - You can change the value of a key in a dictionary.
      
      - example:
  
          ```python
          person = {"name": "Alice", "age": 30}
          person["age"] = 31
          print(person) # prints {"name": "Alice", "age": 31}
          ```

  - You can add a new key-value pair to a dictionary.

    - example:

        ```python
        person = {"name": "Alice", "age": 30}
        person["city"] = "New York"
        print(person) # prints {"name": "Alice", "age": 30, "city": "New York"}
        ```

  - You can remove a key-value pair from a dictionary using the `pop()` method.


    - example:

        ```python
        person = {"name": "Alice", "age": 30}
        person.pop("age")
        print(person) # prints {"name": "Alice"}
        ```
  - You can remove a key-value pair from a dictionary using the `del` keyword.

    - example:

        ```python
        person = {"name": "Alice", "age": 30}
        del person["age"]
        print(person) # prints {"name": "Alice"}
        ```

  - You can clear a dictionary using the `clear()` method.

    - example:

        ```python
        person = {"name": "Alice", "age": 30}
        person.clear()
        print(person) # prints {}
        ```

  - You can copy a dictionary using the `copy()` method.

    - example:

        ```python
        person = {"name": "Alice", "age": 30}
        person_copy = person.copy()
        print(person_copy) # prints {"name": "Alice", "age": 30}
        ```

  - You can create a dictionary using the `dict()` function.

    - example:

        ```python
        person = dict(name="Alice", age=30)
        print(person) # prints {"name": "Alice", "age": 30}
        ```
  - You can create a dictionary using the `fromkeys()` method.

    - example:

        ```python
        keys = ["name", "age"]
        person = dict.fromkeys(keys)
        print(person) # prints {"name": None, "age": None}
        ```

  - You can create a dictionary using the `items()` method.
  
      - example:
  
          ```python
          person = {"name": "Alice", "age": 30}
          items = person.items()
          print(items) # prints dict_items([("name", "Alice"), ("age", 30)])
          ```

  - You can create a dictionary using the `keys()` method.

    - example:

        ```python
        person = {"name": "Alice", "age": 30}
        keys = person.keys()
        print(keys) # prints dict_keys(["name", "age"])
        ```


- To check the type of a variable, use the `type()` function.

- To convert a variable to a different type, use the built-in functions `int()`, `float()`, `str()`, `list()`, `tuple()`, `dict()`, etc.

- Booleans are a built-in data type in Python that can have one of two values: `True` or `False`.

  - Values such as empty sequences (lists, tuples, strings, etc.), 0, and None are evaluated as False. Any non-zero number or non-empty sequence is evaluated as True.

  - Booleans are used in conditional statements, such as `if`, `elif`, and `else`.

  - You can use the `bool()` function to convert a value to a boolean.

  - You can use logical operators, such as `and`, `or`, and `not`, to combine boolean values.

  - You can use comparison operators, such as `==`, `!=`, `<`, `>`, `<=`, and `>=`, to compare values.

- None is a special data type in Python that represents the absence of a value.

### Operators

- Operators are used to perform operations on variables and values.

- Python has several types of operators, such as arithmetic, assignment, comparison, logical, identity, membership, and bitwise operators.

- Arithmetic operators are used to perform mathematical operations, such as addition `+`, subtraction `-`, multiplication `*`, division `/`, modulus `%`, exponentiation `**`, and floor division `//`.

- Assignment operators are used to assign values to variables, such as `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`, and `//=`.

- Comparison operators are used to compare values, such as `==`, `!=`, `<`, `>`, `<=`, and `>=`.

- Logical operators are used to combine boolean values, such as `and`, `or`, and `not`.

- Identity operators are used to compare objects, such as `is` and `is not`.

- Membership operators are used to test if a value is present in a sequence, such as `in` and `not in`.

- Bitwise operators are used to perform bitwise operations on integers, such as `&`, `|`, `^`, `~`, `<<`, and `>>`.

### Control Structures

- Control structures are used to control the flow of a program.

- Python has several types of control structures, such as conditional statements, loops, and function calls.

- Conditional statements are used to execute code based on a condition, such as `if`, `elif`, and `else`.

- Loops are used to execute code repeatedly, such as `for` and `while` loops.

- Function calls are used to execute a block of code that is defined elsewhere in the program.

- You can use the `pass` statement to do nothing in a block of code.

- You can use the `break` statement to exit a loop.

- You can use the `continue` statement to skip the rest of a loop and continue with the next iteration.

- You can use the `return` statement to return a value from a function.

### Functions

- Functions are used to group code into reusable blocks.

- Functions are defined using the `def` keyword, followed by the function name and a pair of parentheses.

- You can pass arguments to a function by placing them inside the parentheses.

- You can return a value from a function using the `return` keyword.

- You can define default values for function arguments by using the assignment operator `=`.

- You can pass a variable number of arguments to a function by using the `*args` and `**kwargs` syntax.

- You can define anonymous functions using the `lambda` keyword.

- You can call a function by using the function name followed by a pair of parentheses.

- You can use the `help()` function to get information about a function.

### Statements

- Statements are used to perform actions in a program.

- Python has several types of statements, such as assignment statements, import statements, print statements, and pass statements.

- Assignment statements are used to assign values to variables.

- Import statements are used to import modules into a program.

- Print statements are used to print output to the console.

- Pass statements are used to do nothing in a block of code.

- You can use the `if` statement to execute code based on a condition.
     
     - example:

        ```python
        x = 10
        if x > 5:
            print("x is greater than 5")
        ```

- You can use the `elif` statement to execute code if the previous condition is False.

    - example:

        ```python
        x = 10
        if x > 5:
            print("x is greater than 5")
        elif x < 5:
            print("x is less than 5")
        ```

- You can use the `else` statement to execute code if all previous conditions are False.

    - example:

        ```python
        x = 10
        if x > 5:
            print("x is greater than 5")
        else:
            print("x is less than or equal to 5")
        ```

- You can use the `for` statement to iterate over a sequence of items.

    - example:

        ```python
        fruits = ["apple", "banana", "cherry"]
        for fruit in fruits:
            print(fruit)
        ```

- You can use the `while` statement to execute code as long as a condition is True.

    - example:

        ```python
        x = 0
        while x < 5:
            print(x)
            x += 1
        ```

- You can use the `try` statement to catch exceptions in a program.

    - example:

        ```python
        try:
            x = 1 / 0
        except ZeroDivisionError:
            print("Cannot divide by zero")
        ```

- You can use the `with` statement to open and close files in a program.
  
    - example:

        ```python
        with open("file.txt", "r") as file:
            content = file.read()
            print(content)
        ```
- You can use the `assert` statement to check if an expression is True. 

    - example:

        ```python
        x = 10
        assert x > 5, "x is not greater than 5"
        ```

- You can use the `yield` statement to return a value from a generator function.

    - example:

        ```python
        def numbers():
            yield 1
            yield 2
            yield 3

        for number in numbers():
            print(number) # outputs 1, 2, 3
        ```

- You can use the `raise` statement to raise an exception in a program.

    - example:

        ```python
        x = -1
        if x < 0:
            raise ValueError("x cannot be negative")
        ```

- You can use the `global` statement to access a global variable inside a function.

    - example:

        ```python
        x = 10

        def print_x():
            global x
            print(x)

        print_x() # prints 10
        ```

- You can use the `nonlocal` statement to access a variable in the outer scope of a function.

    - example:

        ```python
        def outer():
            x = 10

            def inner():
                nonlocal x
                x += 1
                print(x)

            inner()

        outer() # prints 11
        ```

  - global vs non-local variables

    - Global variables are defined outside of functions and can be accessed inside functions using the `global` keyword.

    - Non-local variables are defined in the outer scope of a function and can be accessed inside nested functions using the `nonlocal` keyword.

        - example: 

            ```python
            x = 10

            def outer():
                x = 20

                def inner():
                    nonlocal x
                    x += 1
                    print(x)

                inner()

            outer() # prints 21
            ```

    - The `global` keyword is used to access a global variable inside a function.

    - The `nonlocal` keyword is used to access a variable in the outer scope of a function.

- You can use the `pass` statement to do nothing in a block of code.

- You can use the `break` statement to exit a loop.

- You can use the `continue` statement to skip the rest of a loop and continue with the next iteration.

- You can use the `return` statement to return a value from a function.



### Functions

- Functions are used to group code into reusable blocks.

- Functions are defined using the `def` keyword, followed by the function name and a pair of parentheses.

     - example:

        ```python
        def greet():
            print("Hello, World!")

        greet() # prints Hello, World!
        ```
- You can pass arguments to a function by placing them inside the parentheses.

    - example:

        ```python
        def greet(name):
            print(f"Hello, {name}!")

        greet("Alice") # prints Hello, Alice!
        ```
- You can return a value from a function using the `return` keyword.

    - example:

        ```python
        def add(a, b):
            return a + b

        result = add(1, 2)
        print(result) # prints 3
        ```
- You can define default values for function arguments by using the assignment operator `=`.
  
    - example:

        ```python
        def greet(name="World"):
            print(f"Hello, {name}!")

        greet() # prints Hello, World!
        greet("Alice") # prints Hello, Alice!
        ``` 

- You can pass a variable number of arguments to a function by using the `*args` and `**kwargs` syntax. 

    - example:

        ```python
        def add(*args):
            return sum(args)

        result = add(1, 2, 3, 4, 5)
        print(result) # prints 15
        ``` 
    - example for kwargs:
      
        ```python
        def greet(**kwargs):
            for key, value in kwargs.items():
                print(f"{key}: {value}")

        greet(name="Alice", age=30) # prints name: Alice and age: 30
        ```
- You can define anonymous functions using the `lambda` keyword.  

    - example:

        ```python
        add = lambda a, b: a + b
        result = add(1, 2)
        print(result) # prints 3
        ```

- You can call a function by using the function name followed by a pair of parentheses.

    - example:

        ```python
        def greet():
            print("Hello, World!")

        greet() # prints Hello, World!
        ```
- You can use the `help()` function to get information about a function.
  
    - example:

        ```python
        def greet(name):
            print(f"Hello, {name}!")

        help(greet)
        ```
- function parameters vs arguments
  
    - Parameters are the names used in the function definition to refer to the arguments passed to the function.

    - Arguments are the values passed to the function when it is called.

    - example:
  
        ```python
        def greet(name):
            print(f"Hello, {name}!")

        greet("Alice") # Alice is the argument passed to the greet function
        ```

- keyword parameters vs positional parameters

  - Positional parameters are passed to a function based on their position in the function call.

  - Keyword parameters are passed to a function based on their name in the function call.

  - example:
  
      ```python
    def greet(name, age):
        print(f"Hello, {name}! You are {age} years old.")

    greet("Alice", 30) # Alice is the name and 30 is the age
    greet(age=30, name="Alice") # Alice is the name and 30 is the age
      ```

- default parameters
  
    - Default parameters are used to provide a default value for a parameter if no value is passed to the function.
    
        - example:
    
            ```python
            def greet(name="World"):
                print(f"Hello, {name}!")

            greet() # prints Hello, World!
            greet("Alice") # prints Hello, Alice!
            ```

- variable number of arguments
  
    - You can pass a variable number of arguments to a function by using the `*args` and `**kwargs` syntax.
  
      - example:
  
          ```python
            def add(*args):
                return sum(args)
  
            result = add(1, 2, 3, 4, 5)
            print(result) # prints 15
        ```
      - example:

        ```python
        def greet(**kwargs):
            for key, value in kwargs.items():
                print(f"{key}: {value}")

        greet(name="Alice", age=30) # prints name: Alice and age: 30
        ```
- anonymous functions
    
    - You can define anonymous functions using the `lambda` keyword.
      
      - example:
      
          ```python
          add = lambda a, b: a + b
          result = add(1, 2)
          print(result) # prints 3
          ```   

- function scope

    - The scope of a variable refers to the region of a program where the variable is accessible.
  
    - Variables defined inside a function are local to that function and cannot be accessed outside the function.
  
    - Variables defined outside a function are global and can be accessed inside the function using the `global` keyword.
  
        - example:
  
            ```python
            x = 10

            def print_x():
                global x
                print(x)

            print_x() # prints 10
            ```

- Function Recursion
  
    - Recursion is a technique in which a function calls itself to solve a problem.
  
    - Recursion is used to break a complex problem into smaller subproblems that are easier to solve.
  
    - Recursion consists of two parts: the base case and the recursive case.
  
    - The base case is the condition that stops the recursion.
  
    - The recursive case is the condition that calls the function recursively.
    
      - example:

          ```python
          def factorial(n):
              if n == 0:
                  return 1
              else:
                  return n * factorial(n - 1)

          result = factorial(5)
          print(result) # prints 120
          ```

- Function Decorators
  
    - Function decorators are used to modify the behavior of a function or method.

    - Function decorators are defined using the `@` symbol followed by the decorator name.

    - Function decorators take a function as an argument and return a new function.

    - Function decorators are used to add functionality to a function without modifying its code.

        - example:

            ```python
            def uppercase(func):
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    return result.upper()
                return wrapper

            @uppercase
            def greet(name):
                return f"Hello, {name}!"

            result = greet("Alice")
            print(result) # prints HELLO, ALICE!
            ```

- Function Generators
    
  - Function generators are used to create iterators in Python.

  - Function generators are defined using the `yield` keyword.

  - Function generators return a generator object that can be iterated over.

  - Function generators are used to generate a sequence of values without storing them in memory.

      - example:

          ```python
          def numbers():
              yield 1
              yield 2
              yield 3

          for number in numbers():
              print(number) # outputs 1, 2, 3
          ```

- Function Annotations
    
  - Function annotations are used to provide additional information about the types of function parameters and return values.

  - Function annotations are defined using a colon `:` after the parameter name or return value, followed by the annotation type.

  - Function annotations are optional and do not affect the behavior of the function.

      - example:

          ```python
          def add(a: int, b: int) -> int:
              return a + b
          ```

- Function Arguments
      
  - Function arguments are the values passed to a function when it is called.

  - Function arguments can be passed by position or by keyword.

  - Function arguments can have default values.

  - Function arguments can be passed as a variable number of arguments using the `*args` and `**kwargs` syntax.

      - example:

          ```python
          def greet(name):
              print(f"Hello, {name}!")

          greet("Alice") # Alice is the argument passed to the greet function
          ```

- Function Parameters

- Function parameters are the names used in the function definition to refer to the arguments passed to the function.

- Function parameters can have default values.

- Function parameters can be passed by position or by keyword.

    - example:

        ```python
        def greet(name):
            print(f"Hello, {name}!")

        greet("Alice") # Alice is the argument passed to the greet function
        ```

### Modules

- Modules are used to organize code into separate files.

- Modules are defined using the `import` keyword followed by the module name.

- You can import specific functions or variables from a module using the `from` keyword.
  - example:
  
      ```python
      import math

      print(math.pi) # prints 3.141592653589793
      ```
- You can import all functions and variables from a module using the `*` operator.

  - example:

      ```python
      from math import *

      print(pi) # prints 3.141592653589793
      ```
- You can create your own modules by defining functions and variables in a separate file.

- You can import your own modules using the `import` keyword.

- You can use the `as` keyword to create an alias for a module.

  - example:

      ```python
      import math as m

      print(m.pi) # prints 3.141592653589793
      ```
- You can use the `dir()` function to get a list of all functions and variables in a module.
  
    - example:
  
        ```python
        import math
  
        print(dir(math))
        ```
- You can use the `help()` function to get information about a module.
  
    - example:
  
        ```python
        import math
  
        help(math)
        ```
- You can use the `__name__` variable to get the name of a module.
  
    - example:
  
        ```python
        print(__name__) # prints __main__ if the module is run directly
        ```
- You can use the `__file__` variable to get the path to a module.

  - example:

      ```python
      import math

      print(math.__file__)
      ```
- You can use the `__doc__` variable to get the documentation of a module.

  - example:

      ```python
      import math

      print(math.__doc__)
      ``` 

- You can use the `__all__` variable to specify which functions and variables to import from a module.
  
    - example:
  
        ```python
        __all__ = ["pi", "e"]
        ``` 

- You can use the `__init__.py` file to define a package in Python.

- You can use the `from` keyword to import a module from a package.

- You can use the `as` keyword to create an alias for a module in a package.


### Classes

- Classes are used to create objects in Python.

- Classes are defined using the `class` keyword followed by the class name.
 
   - example: 

      ```python
      class Person:
          pass
      ```

- You can create an object of a class by calling the class name followed by a pair of parentheses.
  
    - example:
  
        ```python
        class Person:
            pass
  
        person = Person()
        ```

- You can define attributes for a class by assigning values to variables inside the class definition.

    - example:

        ```python
        class Person:
            name = "Alice"
            age = 30
        ```

- You can access attributes of an object using the dot `.` operator.
  
    - example:

        ```python
        class Person:
            name = "Alice"
            age = 30

        person = Person()
        print(person.name) # prints Alice
        print(person.age) # prints 30
        ``` 

- You can define methods for a class by defining functions inside the class definition.
  
    - example:

        ```python
        class Person:
            def greet(self):
                print("Hello, World!")

        person = Person()
        person.greet() # prints Hello, World!
        ```

- You can pass arguments to a method by placing them inside the parentheses.

    - example:

        ```python
        class Person:
            def greet(self, name):
                print(f"Hello, {name}!")

        person = Person()
        person.greet("Alice") # prints Hello, Alice!
        ```

- You can access attributes of an object using the `self` keyword.

    - example:

        ```python
        class Person:
            def greet(self):
                print(f"Hello, {self.name}!")

        person = Person()
        person.name = "Alice"
        person.greet() # prints Hello, Alice!
        ```

- You can define a constructor for a class using the `__init__` method.

  - example:

      ```python
      class Person:
          def __init__(self, name, age):
              self.name = name
              self.age = age

          def greet(self):
              print(f"Hello, {self.name}!")

      person = Person("Alice", 30)
      person.greet() # prints Hello, Alice!
      ```

- You can define a destructor for a class using the `__del__` method.

  - example:

      ```python
      class Person:
          def __del__(self):
              print("Object deleted")

      person = Person()
      del person # prints Object deleted
      ```

- You can define class attributes by assigning values to variables inside the class definition.

  - example:

      ```python
      class Person:
          count = 0

          def __init__(self):
              Person.count += 1

      person1 = Person()
      person2 = Person()
      print(Person.count) # prints 2
      ```

- You can define class methods using the `@classmethod` decorator.

  - example:

      ```python
      class Person:
          count = 0

          @classmethod
          def increment_count(cls):
              cls.count += 1

      Person.increment_count()
      Person.increment_count()
      print(Person.count) # prints 2
      ```

- You can define static methods using the `@staticmethod` decorator.
  
    - example:
  
        ```python
        class Person:
            @staticmethod
            def greet():
                print("Hello, World!")
  
        Person.greet() # prints Hello, World!
        ```

- classmethod vs staticmethod 

  - Class methods take a class as the first argument, while static methods do not take any arguments.

  - Class methods can access class variables, while static methods cannot.

  - Class methods are used to modify class variables, while static methods are used to perform utility functions.

      - example:

          ```python
          class Person:
              count = 0

              @classmethod
              def increment_count(cls):
                  cls.count += 1

              @staticmethod
              def greet():
                  print("Hello, World!")

          Person.increment_count()
          Person.increment_count()
          print(Person.count) # prints 2

          Person.greet() # prints Hello, World!
          ```

- You can define properties for a class using the `@property` decorator.

  - example:

      ```python
      class Person:
          def __init__(self, name):
              self._name = name

          @property
          def name(self):
              return self._name

          @name.setter
          def name(self, value):
              self._name = value

      person = Person("Alice")
      print(person.name) # prints Alice

      person.name = "Bob"
      print(person.name) # prints Bob
      ```

- You can define class inheritance by passing the parent class as an argument to the child class.

  - example:

      ```python
      class Person:
          def greet(self):
              print("Hello, World!")

      class Student(Person):
          def study(self):
              print("Studying...")

      student = Student()
      student.greet() # prints Hello, World!
      student.study() # prints Studying...
      ```

- You can override methods of a parent class in a child class.  

    - example:

        ```python
        class Person:
            def greet(self):
                print("Hello, World!")

        class Student(Person):
            def greet(self):
                print("Hello, Student!")

        student = Student()
        student.greet() # prints Hello, Student!
        ```

- You can call the parent class constructor
  - example:
  
      ```python
      class Person:
          def __init__(self, name):
              self.name = name

      class Student(Person):
          def __init__(self, name, grade):
              super().__init__(name)
              self.grade = grade

      student = Student("Alice", 10)
      print(student.name) # prints Alice
      print(student.grade) # prints 10
      ```

- You can use multiple inheritance by passing multiple parent classes to the child class.

  - example:

      ```python
      class A:
          def greet(self):
              print("Hello, A!")

      class B:
          def greet(self):
              print("Hello, B!")

      class C(A, B):
          pass

      c = C()
      c.greet() # prints Hello, A!
      ```

- You can use the `super()` function to call methods of a parent class.

  - example:

      ```python
      class A:
          def greet(self):
              print("Hello, A!")

      class B(A):
          def greet(self):
              super().greet()
              print("Hello, B!")

      b = B()
      b.greet() # prints Hello, A! and Hello, B!
      ```

- You can use the `isinstance()` function to check if an object is an instance of a class.

  - example:

      ```python
      class Person:
          pass

      person = Person()
      print(isinstance(person, Person)) # prints True
      ```
- You can use the `issubclass()` function

  - example:

      ```python
      class A:
          pass

      class B(A):
          pass

      print(issubclass(B, A)) # prints True
      ```
- You can use the `hasattr()` function to check if an object has an attribute.  

    - example:

        ```python
        class Person:
            name = "Alice"

        person = Person()
        print(hasattr(person, "name")) # prints True
        ```

- You can use the `getattr()` function to get the value of an attribute.


    - example:

        ```python
        class Person:
            name = "Alice"

        person = Person()
        print(getattr(person, "name")) # prints Alice
        ```

- You can use the `setattr()` function to set the value of an attribute.

    - example:

        ```python
        class Person:
            name = "Alice"

        person = Person()
        setattr(person, "name", "Bob")
        print(person.name) # prints Bob
        ```

- You can use the `delattr()` function to delete an attribute.

    - example:

        ```python
        class Person:
            name = "Alice"

        person = Person()
        delattr(person, "name")
        print(hasattr(person, "name")) # prints False
        ```
- You can use the `property()` function to define properties for a class.

    - example:

        ```python
        class Person:
            def __init__(self, name):
                self._name = name

            def get_name(self):
                return self._name

            def set_name(self, value):
                self._name = value

            name = property(get_name, set_name)

        person = Person("Alice")
        print(person.name) # prints Alice

        person.name = "Bob"
        print(person.name) # prints Bob
        ```


### Exceptions

- Exceptions are used to handle errors in a program.
  - example:
  
      ```python
      try:
          x = 1 / 0
      except ZeroDivisionError:
          print("Cannot divide by zero")
      ```

- Exceptions are raised when an error occurs in a program.

  - example:

      ```python
      x = 1 / 0
      ```

- You can catch exceptions using the `try` and `except` blocks.

  - example:

      ```python
      try:
          x = 1 / 0
      except ZeroDivisionError:
          print("Cannot divide by zero")
      ```

- You can catch multiple exceptions using the `except` block.
  
    - example:
  
        ```python
        try:
            x = 1 / 0
        except ZeroDivisionError:
            print("Cannot divide by zero")
        except ValueError:
            print("Invalid value")
        ```

- You can use the `else` block to execute code if no exceptions are raised.
  
    - example:
  
        ```python
        try:
            x = 1 / 1
        except ZeroDivisionError:
            print("Cannot divide by zero")
        else:
            print("Division successful")
        ```

- You can use the `finally` block to execute code after the `try` block, regardless of whether an exception is raised.

  - example:

      ```python
      try:
          x = 1 / 0
      except ZeroDivisionError:
          print("Cannot divide by zero")
      finally:
          print("Done")
      ```

- You can raise exceptions using the `raise` keyword.
  
    - example:
  
        ```python
        x = -1
        if x < 0:
            raise ValueError("x cannot be negative")
        ```

- You can create custom exceptions by defining a new class that inherits from the `Exception` class.

  - example:

      ```python
      class NegativeValueError(Exception):
          pass

      x = -1
      if x < 0:
          raise NegativeValueError("x cannot be negative")
      ```

- You can use the `assert` statement to check if an expression is True.

  - example:

      ```python
      x = 10
      assert x > 5, "x is not greater than 5"
      ```

### File I/O

- File I/O is used to read from and write to files in Python.

- You can open a file using the `open()` function.

  - example:

      ```python
      file = open("file.txt", "r")
      ```
- You can read from a file using the `read()` method.
  
    - example:
  
        ```python
        file = open("file.txt", "r")
        content = file.read()
        print(content)
        ```
- You can write to a file using the `write()` method.
  
    - example:
  
        ```python
        file = open("file.txt", "w")
        file.write("Hello, World!")
        file.close()
        ```
- You can read a file line by line using the `readline()` method.
    
    - example:
  
        ```python
        file = open("file.txt", "r")
        line = file.readline()
        print(line)
        ```
- You can write to a file line by line using the `writelines()` method.
    
    - example:
  
        ```python
        file = open("file.txt", "w")
        lines = ["Hello, World!", "Goodbye, World!"]
        file.writelines(lines)
        file.close()
        ```

- You can close a file using the `close()` method.

  - example:

      ```python
      file = open("file.txt", "r")
      file.close()
      ```
- You can use the `with` statement to open and close files in a program.

  - example:

      ```python
      with open("file.txt", "r") as file:
          content = file.read()
          print(content)
      ```
- You can use the `readlines()` method to read all lines from a file into a list.

  - example:

      ```python
      with open("file.txt", "r") as file:
          lines = file.readlines()
          for line in lines:
              print(line)
      ```
- You can use the `seek()` method to change the file cursor position.
  
    - example:
  
        ```python
        with open("file.txt", "r") as file:
            file.seek(5)
            content = file.read()
            print(content)
        ```
- You can use the `tell()` method to get the current file cursor position.

  - example:

      ```python
      with open("file.txt", "r") as file:
          position = file.tell()
          print(position)
      ```
- You can use the `truncate()` method to truncate a file to a specified size.
  
    - example:
  
        ```python
        with open("file.txt", "r+") as file:
            file.truncate(5)
        ```
- You can use the `mode` parameter to specify the file mode when opening a file.
  
    - example:
  
        ```python
        file = open("file.txt", "r")
        ```
- You can use the `encoding` parameter to specify the file encoding when opening a file.
  
    - example:
  
        ```python
        file = open("file.txt", "r", encoding="utf-8")
        ```
- You can use the `newline` parameter to specify the newline character when opening a file.
    
    - example:
  
        ```python
        file = open("file.txt", "r", newline="")
        ```

- You can use the `os` module to work with files and directories in Python.

- You can use the `os.path` module to work with file paths in Python.

    - example:

        ```python
        import os

        path = "file.txt"
        print(os.path.exists(path)) # prints True
        print(os.path.isfile(path)) # prints True
        print(os.path.isdir(path)) # prints False
        ```

- You can use the `os.path.join()` function to join two or more paths.

    - example:

        ```python
        import os

        path1 = "dir1"
        path2 = "dir2"
        path = os.path.join(path1, path2)
        print(path) # prints dir1/dir2
        ```

- You can use the `os.path.basename()` function to get the base name of a path.
  
    - example:

        ```python
        import os

        path = "dir/file.txt"
        basename = os.path.basename(path)
        print(basename) # prints file.txt
        ```

- You can use the `os.path.dirname()` function to get the directory name of a path.

    - example:

        ```python
        import os

        path = "dir/file.txt"
        dirname = os.path.dirname(path)
        print(dirname) # prints dir
        ```

- You can use the `os.path.abspath()` function to get the absolute path of a file.

    - example:

        ```python
        import os

        path = "file.txt"
        abspath = os.path.abspath(path)
        print(abspath) # prints /path/to/file.txt
        ```

- You can use the `os.path.exists()` function to check if a file or directory exists.

    - example:

        ```python
        import os

        path = "file.txt"
        print(os.path.exists(path)) # prints True
        ```

- You can use the `os.path.isfile()` function to check if a path is a file.

    - example:

        ```python
        import os

        path = "file.txt"
        print(os.path.isfile(path)) # prints True
        ```
- You can use the `os.path.isdir()` function to check if a path is a directory.

    - example:

        ```python
        import os

        path = "dir"
        print(os.path.isdir(path)) # prints True
        ```

- You can use the `os.path.getsize()` function to get the size of a file in bytes.

    - example:

        ```python
        import os

        path = "file.txt"
        size = os.path.getsize(path)
        print(size) # prints 10
        ```

- You can use the `os.path.getmtime()` function to get the last modified time of a file.
  
    - example:

        ```python
        import os

        path = "file.txt"
        mtime = os.path.getmtime(path)
        print(mtime) # prints 1630000000.0
        ```

- You can use the `os.path.getctime()` function to get the creation time of a file.

    - example:

        ```python
        import os

        path = "file.txt"
        ctime = os.path.getctime(path)
        print(ctime) # prints 1630000000.0
        ```

- You can use the `os.listdir()` function to get a list of files and directories in a directory.

    - example:

        ```python
        import os

        path = "dir"
        files = os.listdir(path)
        print(files) # prints ["file1.txt", "file2.txt"]
        ```
- You can use the `os.mkdir()` function to create a directory.

    - example:

        ```python
        import os

        path = "dir"
        os.mkdir(path)
        ```
- You can use the `os.makedirs()` function to create a directory and its parent directories.
  
    - example:

        ```python
        import os

        path = "dir1/dir2"
        os.makedirs(path)
        ``` 

- You can use the `os.remove()` function to delete a file.

    - example:

        ```python
        import os

        path = "file.txt"
        os.remove(path)
        ```

- You can use the `os.rmdir()` function to delete a directory.

    - example:

        ```python
        import os

        path = "dir"
        os.rmdir(path)
        ```

- You can use the `os.removedirs()` function to delete a directory and its parent directories.

    - example:

        ```python
        import os

        path = "dir1/dir2"
        os.removedirs(path)
        ```

- You can use the `os.rename()` function to rename a file or directory.

    - example:

        ```python
        import os

        old_path = "file.txt"
        new_path = "new_file.txt"
        os.rename(old_path, new_path)
        ```

- You can use the `os.walk()` function to iterate over all files and directories in a directory.

    - example:

        ```python
        import os

        path = "dir"
        for root, dirs, files in os.walk(path):
            print(root)
            print(dirs)
            print(files)
        ```

- You can use the `shutil` module to work with files and directories in Python.

- You can use the `shutil.copy()` function to copy a file.

    - example:

        ```python
        import shutil

        src = "file.txt"
        dst = "new_file.txt"
        shutil.copy(src, dst)
        ```
- You can use the `shutil.copytree()` function to copy a directory.
  
    - example:

        ```python
        import shutil

        src = "dir"
        dst = "new_dir"
        shutil.copytree(src, dst)
        ```

- You can use the `shutil.move()` function to move a file or directory.

    - example:

        ```python
        import shutil

        src = "file.txt"
        dst = "new_file.txt"
        shutil.move(src, dst)
        ```

- You can use the `shutil.rmtree()` function to delete a directory and its contents.

    - example:

        ```python
        import shutil

        path = "dir"
        shutil.rmtree(path)
        ```

- You can use the `shutil.make_archive()` function to create a zip archive of a directory.
  
    - example:

        ```python
        import shutil

        path = "dir"
        shutil.make_archive("archive", "zip", path)
        ```
- You can use the `shutil.unpack_archive()` function to extract a zip archive.
  
    - example:

        ```python
        import shutil

        path = "archive.zip"
        shutil.unpack_archive(path)
        ```
- You can use the `shutil.disk_usage()` function to get disk usage statistics.
  
    - example:

        ```python
        import shutil

        path = "dir"
        usage = shutil.disk_usage(path)
        print(usage)
        ```

- You can use the `shutil.which()` function to find the path to an executable.

    - example:

        ```python
        import shutil

        path = "python"
        print(shutil.which(path))
        ```
- You can use the `shutil.get_terminal_size()` function to get the size of the terminal window.

    - example:

        ```python
        import shutil

        size = shutil.get_terminal_size()
        print(size)
        ```

- You can use the `shutil.get_archive_formats()` function to get a list of supported archive formats.

    - example:

        ```python
        import shutil

        formats = shutil.get_archive_formats()
        print(formats)
        ```

- You can use the `shutil.get_unpack_formats()` function to get a list of supported unpack formats.

    - example:

        ```python
        import shutil

        formats = shutil.get_unpack_formats()
        print(formats)
        ```

- You can use the `shutil.register_archive_format()` function to register a new archive format.

    - example:

        ```python
        import shutil

        def extract_zip(filename, extract_dir):
            pass

        shutil.register_archive_format("zip", extract_zip)
        ```

- You can use the `shutil.register_unpack_format()` function to register a new unpack format.

    - example:

        ```python
        import shutil

        def extract_zip(filename, extract_dir):
            pass

        shutil.register_unpack_format("zip", extract_zip)
        ```

- You can use the `shutil.unregister_archive_format()` function to unregister an archive format.  

    - example:

        ```python
        import shutil

        shutil.unregister_archive_format("zip")
        ```

- You can use the `shutil.unregister_unpack_format()` function to unregister an unpack format.

    - example:

        ```python
        import shutil

        shutil.unregister_unpack_format("zip")
        ```

- You can use the `shutil.get_terminal_size()` function to get the size of the terminal window.


### Regular Expressions

- Regular expressions are used to search for patterns in text.

- Regular expressions are defined using the `re` module.
  
    - example:
  
        ```python
        import re
        ```
- You can use the `re.search()` function to search for a pattern in a string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "World"
        match = re.search(pattern, text)
        print(match.group()) # prints World
        ```

- You can use the `re.match()` function to match a pattern at the beginning of a string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "Hello"
        match = re.match(pattern, text)
        print(match.group()) # prints Hello
        ``` 

- You can use the `re.findall()` function to find all occurrences of a pattern in a string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "l"
        matches = re.findall(pattern, text)
        print(matches) # prints ['l', 'l', 'l']
        ```

- You can use the `re.sub()` function to replace occurrences of a pattern in a string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "World"
        replacement = "Alice"
        new_text = re.sub(pattern, replacement, text)
        print(new_text) # prints Hello, Alice!
        ```

- You can use special characters in regular expressions to match specific patterns.

- You can use the `.` character to match any character.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "H.llo"
        match = re.search(pattern, text)
        print(match.group()) # prints Hello
        ``` 

- You can use the `^` character to match the beginning of a string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "^Hello"
        match = re.match(pattern, text)
        print(match.group()) # prints Hello
        ```

- You can use the `$` character to match the end of a string.
  
    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "World!$"
        match = re.search(pattern, text)
        print(match.group()) # prints World!
        ```

- You can use the `*` character to match zero or more occurrences of a pattern.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "l*"
        matches = re.findall(pattern, text)
        print(matches) # prints ['', '', 'l',

        ``` 

- You can use the `+` character to match one or more occurrences of a pattern.


    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "l+"
        matches = re.findall(pattern, text)
        print(matches) # prints ['l', 'l', 'l']
        ```

- You can use the `?` character to match zero or one occurrence of a pattern.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "l?"
        matches = re.findall(pattern, text)
        print(matches) # prints ['', 'l', '', 'l', 'l', '', '']
        ```

- You can use the `{n}` character to match exactly `n` occurrences of a pattern.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "l{2}"
        matches = re.findall(pattern, text)
        print(matches) # prints ['ll']
        ```

- You can use the `{n, m}` character to match between `n` and `m` occurrences of a pattern.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "l{1,2}"
        matches = re.findall(pattern, text)
        print(matches) # prints ['l', 'l', 'l']
        ```

- You can use the `[]` character to match any character in a set.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "[aeiou]"
        matches = re.findall(pattern, text)
        print(matches) # prints ['e', 'o', 'o']
        ```

- You can use the `[^]` character to match any character not in a set.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "[^aeiou]"
        matches = re.findall(pattern, text)
        print(matches) # prints ['H', 'l', 'l', ',', ' ', 'W', 'r', 'l', 'd', '!']
        ```

- You can use the `|` character to match either of two patterns.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "Hello|World"
        match = re.search(pattern, text)
        print(match.group()) # prints Hello
        ```

- You can use the `\d` character to match any digit.

    - example:

        ```python
        import re

        text = "Hello, 123!"
        pattern = "\d"
        matches = re.findall(pattern, text)
        print(matches) # prints ['1', '2', '3']
        ```
- You can use the `\D` character to match any non-digit.
  
    - example:

        ```python
        import re

        text = "Hello, 123!"
        pattern = "\D"
        matches = re.findall(pattern, text)
        print(matches) # prints ['H', 'e', 'l', 'l', 'o', ',', ' ', '!']
        ``` 

- You can use the `\w` character to match any word character.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "\w"
        matches = re.findall(pattern, text)
        print(matches) # prints ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']
        ```
- You can use the `\W` character to match any non-word character.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "\W"
        matches = re.findall(pattern, text)
        print(matches) # prints [',', ' ', '!']
        ```
- You can use the `\s` character to match any whitespace character.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "\s"
        matches = re.findall(pattern, text)
        print(matches) # prints [',', ' ']
        ```

- You can use the `\S` character to match any non-whitespace character.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "\S"
        matches = re.findall(pattern, text)
        print(matches) # prints ['H', 'e', 'l', 'l', 'o', ',', 'W', 'o', 'r', 'l', 'd', '!']
        ```

- You can use the `re.IGNORECASE` flag to perform case-insensitive matching.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "hello"
        match = re.search(pattern, text, re.IGNORECASE)
        print(match.group()) # prints Hello
        ```

- You can use the `re.MULTILINE` flag to match the beginning and end of each line.

    - example:

        ```python
        import re

        text = "Hello\nWorld"
        pattern = "^Hello"
        match = re.search(pattern, text, re.MULTILINE)
        print(match.group()) # prints Hello
        ```

- You can use the `re.DOTALL` flag to match any character, including newlines.

    - example:

        ```python
        import re

        text = "Hello\nWorld"
        pattern = "Hello.World"
        match = re.search(pattern, text, re.DOTALL)
        print(match.group()) # prints Hello\nWorld
        ```

- You can use the `re.VERBOSE` flag to write regular expressions in a more readable format.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = """
        Hello # match Hello
        , # match comma
        World # match World
        """
        match = re.search(pattern, text, re.VERBOSE)
        print(match.group()) # prints Hello, World
        ```

- You can use the `re.compile()` function to compile a regular expression.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = re.compile("World")
        match = pattern.search(text)
        print(match.group()) # prints World
        ```

- You can use the `re.split()` function to split a string using a regular expression.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = ","
        parts = re.split(pattern, text)
        print(parts) # prints ['Hello', ' World!']
        ```

- You can use the `re.escape()` function to escape special characters in a string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = re.escape("Hello, World!")
        match = re.search(pattern, text)
        print(match.group()) # prints Hello, World!
        ```
- You can use the `re.fullmatch()` function to match the entire string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "Hello, World!"
        match = re.fullmatch(pattern, text)
        print(match.group()) # prints Hello, World!
        ```

- You can use the `re.finditer()` function to find all occurrences of a pattern in a string.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "l"
        matches = re.finditer(pattern, text)
        for match in matches:
            print(match.group())
        ```

- You can use the `re.subn()` function to replace occurrences of a pattern in a string and get the number of replacements.

    - example:

        ```python
        import re

        text = "Hello, World!"
        pattern = "World"
        replacement = "Alice"
        new_text, count = re.subn(pattern, replacement, text)
        print(new_text) # prints Hello, Alice!
        print(count) # prints 1
        ```

### Testing

- Testing is used to verify that a program works as expected.

- You can use the `unittest` module to write tests in Python.

- You can create a test case by creating a class that inherits from `unittest.TestCase`.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertEqual(1 + 1, 2)
        ```

- You can use the `assertEqual()` method to check if two values are equal.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertEqual(1 + 1, 2)
        ```

- You can use the `assertNotEqual()` method to check if two values are not equal.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertNotEqual(1 + 1, 3)
        ```

- You can use the `assertTrue()` method to check if a value is True.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertTrue(1 + 1 == 2)
        ```

- You can use the `assertFalse()` method to check if a value is False.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertFalse(1 + 1 == 3)
        ```

- You can use the `assertIn()` method to check if a value is in a list.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertIn(1, [1, 2, 3])
        ```


- You can use the `assertNotIn()` method to check if a value is not in a list.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertNotIn(4, [1, 2, 3])
        ```

- You can use the `assertIs()` method to check if two values are the same object.


    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                x = [1, 2, 3]
                y = x
                self.assertIs(x, y)
        ```


- You can use the `assertIsNot()` method to check if two values are not the same object.


    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                x = [1, 2, 3]
                y = [1, 2, 3]
                self.assertIsNot(x, y)
        ```   

- You can use the `assertRaises()` method to check if an exception is raised.


    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_divide(self):
                with self.assertRaises(ZeroDivisionError):
                    x = 1 / 0
        ```

- You can use the `setUp()` method to run code before each test method.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def setUp(self):
                self.x = 1
                self.y = 2

            def test_add(self):
                self.assertEqual(self.x + self.y, 3)
        ```
- You can use the `tearDown()` method to run code after each test method.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def setUp(self):
                self.x = 1
                self.y = 2

            def tearDown(self):
                del self.x
                del self.y

            def test_add(self):
                self.assertEqual(self.x + self.y, 3)
        ```
- You can use the `@unittest.skip()` decorator to skip a test.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            @unittest.skip("Skip this test")
            def test_add(self):
                self.assertEqual(1 + 1, 2)
        ``` 

- You can use the `@unittest.skipIf()` decorator to skip a test if a condition is True.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            @unittest.skipIf(True, "Skip this test")
            def test_add(self):
                self.assertEqual(1 + 1, 2)
        ```

- You can use the `@unittest.skipUnless()` decorator to skip a test unless a condition is True.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            @unittest.skipUnless(False, "Skip this test")
            def test_add(self):
                self.assertEqual(1 + 1, 2)
        ```
- You can use the `@unittest.expectedFailure()` decorator to mark a test as expected to fail.

    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            @unittest.expectedFailure
            def test_add(self):
                self.assertEqual(1 + 1, 3)
        ```

- You can use the `unittest.main()` function to run tests in a module.



    - example:

        ```python
        import unittest

        class TestMath(unittest.TestCase):
            def test_add(self):
                self.assertEqual(1 + 1, 2)

        if __name__ == "__main__":
            unittest.main()
        ```


### Debugging

- Debugging is the process of finding and fixing errors in a program.

- You can use the `print()` function to print the value of a variable.

    - example:

        ```python
        x = 1
        print(x) # prints 1
        ```
- You can use the `assert` statement to check if a condition is True.

    - example:

        ```python
        x = 1
        assert x == 1
        ```

- You can use the `pdb` module to debug a program.

- You can use the `pdb.set_trace()` function to set a breakpoint in a program.

    - example:

        ```python
        import pdb

        x = 1
        pdb.set_trace()
        y = 2
        ```
- You can use the `pdb` module to step through a program.

- You can use the `n` command to step to the next line.

- You can use the `s` command to step into a function.

- You can use the `c` command to continue running the program.

- You can use the `q` command to quit the debugger.

- You can use the `l` command to list the source code.

- You can use the `p` command to print the value of a variable.

- You can use the `pp` command to pretty-print the value of a variable.

- You can use the `w` command to show the current call stack.

- You can use the `u` command to move up the call stack.

- You can use the `d` command to move down the call stack.

- You can use the `b` command to set a breakpoint.

- You can use the `cl` command to clear a breakpoint.

- You can use the `bt` command to show a traceback.

- You can use the `a` command to print the arguments of the current function.

- You can use the `r` command to return from the current function.

- You can use the `h` command to show help.

- You can use the `?` command to show help.

- You can use the `pdb.run()` function to run a program in the debugger.

    - example:

        ```python
        import pdb

        def add(x, y):
            return x + y

        pdb.run("add(1, 2)")
        ```
- You can use the `pdb.pm()` function to run a program in the debugger.

    - example:

        ```python
        import pdb

        def add(x, y):
            return x + y

        pdb.pm()
        add(1, 2)
        ```

- You can use the `pdb.post_mortem()` function to run a program in the debugger after an exception is raised.

    - example:

        ```python
        import pdb

        def add(x, y):
            return x + y

        try:
            add(1, "2")
        except:
            pdb.post_mortem()
        ```

- You can use the `pdb.set_trace()` function to set a breakpoint in a program.


### Logging

- Logging is used to record events in a program.

- You can use the `logging` module to log messages in Python.

- You can use the `logging.debug()` function to log a debug message.

    - example:

        ```python
        import logging

        logging.basicConfig(level=logging.DEBUG)
        logging.debug("This is a debug message")
        ``` 

- You can use the `logging.info()` function to log an info message.

    - example:

        ```python
        import logging

        logging.basicConfig(level=logging.INFO)
        logging.info("This is an info message")
        ```

- You can use the `logging.warning()` function to log a warning message.  

    - example:

        ```python
        import logging

        logging.basicConfig(level=logging.WARNING)
        logging.warning("This is a warning message")
        ```

- You can use the `logging.error()` function to log an error message.

    - example:

        ```python
        import logging

        logging.basicConfig(level=logging.ERROR)
        logging.error("This is an error message")
        ```
- You can use the `logging.critical()` function to log a critical message.

    - example:

        ```python
        import logging

        logging.basicConfig(level=logging.CRITICAL)
        logging.critical("This is a critical message")
        ```

- You can use the `logging.basicConfig()` function to configure the logging system.

    - example:

        ```python
        import logging

        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.debug("This is a debug message")
        ```
- You can use the `logging.getLogger()` function to get a logger object.
  
    - example:

        ```python
        import logging

        logger = logging.getLogger("my_logger")
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ``` 

- You can use the `logging.Formatter()` class to format log messages.

    - example:

        ```python
        import logging

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```
- You can use the `logging.FileHandler()` class to log messages to a file.

    - example:

        ```python
        import logging

        handler = logging.FileHandler("log.txt")
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```
- You can use the `logging.StreamHandler()` class to log messages to the console.

    - example:

        ```python
        import logging

        handler = logging.StreamHandler()
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```
- You can use the `logging.handlers.RotatingFileHandler()` class to log messages to a file that rotates based on size.

    - example:

        ```python
        import logging
        from logging.handlers import RotatingFileHandler

        handler = RotatingFileHandler("log.txt", maxBytes=1000, backupCount=3)
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```

- You can use the `logging.handlers.TimedRotatingFileHandler()` class to log messages to a file that rotates based on time.

    - example:

        ```python
        import logging
        from logging.handlers import TimedRotatingFileHandler

        handler = TimedRotatingFileHandler("log.txt", when="midnight", interval=1, backupCount=3)
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```

- You can use the `logging.handlers.SysLogHandler()` class to log messages to the system log.

    - example:

        ```python
        import logging
        from logging.handlers import SysLogHandler

        handler = SysLogHandler()
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```

- You can use the `logging.handlers.SMTPHandler()` class to log messages to an email address.

    - example:

        ```python
        import logging
        from logging.handlers import SMTPHandler

        handler = SMTPHandler(mailhost="localhost", fromaddr="", toaddrs="", subject="Log Message")   
        logger = logging.getLogger("my_logger") 
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```

- You can use the `logging.handlers.HTTPHandler()` class to log messages to a web server.

    - example:

        ```python
        import logging
        from logging.handlers import HTTPHandler

        handler = HTTPHandler(host="localhost", url="/log", method="POST")
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```

- You can use the `logging.handlers.QueueHandler()` class to log messages to a queue.


    - example:

        ```python
        import logging
        from logging.handlers import QueueHandler

        handler = QueueHandler()
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        ```

- You can use the `logging.handlers.QueueListener()` class to log messages from a queue.

    - example:

        ```python
        import logging
        from logging.handlers import QueueListener

        handler = logging.StreamHandler()
        listener = QueueListener(queue, handler)
        listener.start()
        logger = logging.getLogger("my_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("This is a debug message")
        listener.stop()
        ```

- You can use the `logging.config.dictConfig()` function to configure the logging system using a dictionary.

    - example:

        ```python
        import logging
        import logging.config

        config = {
            "version": 1,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {
                "my_logger": {
                    "handlers": ["console"],
                    "level": "DEBUG"
                }
            },
            "formatters": {
                "simple": {
                    "format": "%(asctime)s - %(levelname)s - %(message)s"
                }
            }
        }

        logging.config.dictConfig(config)
        logger = logging.getLogger("my_logger")
        logger.debug("This is a debug message")
        ```

- You can use the `logging.config.fileConfig()` function to configure the logging system using a configuration file.

    - example:

        ```python
        import logging
        import logging.config

        logging.config.fileConfig("logging.conf")
        logger = logging.getLogger("my_logger")
        logger.debug("This is a debug message")
        ```

- You can use the `logging.config.listen()` function to configure the logging system using a configuration file.

    - example:

        ```python
        import logging
        import logging.config

        logging.config.listen(9999)
        logger = logging.getLogger("my_logger")
        logger.debug("This is a debug message")
        ```

