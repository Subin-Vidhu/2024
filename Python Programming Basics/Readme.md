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

      example:

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

      example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits.append("orange")
          print(fruits) # prints ["apple", "banana", "cherry", "orange"]
          ```

    - You can insert items into a list at a specific position using the `insert()` method.

      example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits.insert(1, "orange")
          print(fruits) # prints ["apple", "orange", "banana", "cherry"]
          ```

    - You can remove items from a list using the `remove()` method.
      
        example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            fruits.remove("banana")
            print(fruits) # prints ["apple", "cherry"]
            ```

    - You can remove items from a list by index using the `pop()` method.
      
        example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            fruits.pop(1)
            print(fruits) # prints ["apple", "cherry"]
            ```

    - You can remove items from a list by value using the `del` keyword.
      
        example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            del fruits[1]
            print(fruits) # prints ["apple", "cherry"]
            ```

    - You can clear a list using the `clear()` method.
        
          example:
    
              ```python
              fruits = ["apple", "banana", "cherry"]
              fruits.clear()
              print(fruits) # prints []
              ```

    - You can copy a list using the `copy()` method.

      example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits_copy = fruits.copy()
          print(fruits_copy) # prints ["apple", "banana", "cherry"]
          ```

    - You can join two lists using the `extend()` method.
      
        example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            more_fruits = ["orange", "mango", "grape"]
            fruits.extend(more_fruits)
            print(fruits) # prints ["apple", "banana", "cherry", "orange", "mango", "grape"]
            ```

    - You can reverse a list using the `reverse()` method.
        
          example:
    
              ```python
              fruits = ["apple", "banana", "cherry"]
              fruits.reverse()
              print(fruits) # prints ["cherry", "banana", "apple"]
              ```
    - You can sort a list using the `sort()` method.

      example:

          ```python
          fruits = ["banana", "apple", "cherry"]
          fruits.sort()
          print(fruits) # prints ["apple", "banana", "cherry"]
          ```
    - You can count the occurrences of an item in a list using the `count()` method.
    
      example:

          ```python
          fruits = ["apple", "banana", "cherry", "apple"]
          count = fruits.count("apple")
          print(count) # prints 2
          ```
    - You can get the index of an item in a list using the `index()` method.
      
        example:
  
            ```python
            fruits = ["apple", "banana", "cherry"]
            index = fruits.index("banana")
            print(index) # prints 1
            ``` 

    - You can check if an item is in a list using the `in` operator.

      example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          if "banana" in fruits:
              print("Yes")
          else:
              print("No")
          ``` 

    - You can check if a list is empty using the `bool()` function.

      example:

          ```python
          fruits = []
          if fruits:
              print("Yes")
          else:
              print("No")
          ```
    - You can convert a list to a string using the `join()` method.

      example:

          ```python
          fruits = ["apple", "banana", "cherry"]
          fruits_str = ", ".join(fruits)
          print(fruits_str) # prints "apple, banana, cherry"
          ```
    - You can convert a string to a list using the `split()` method.

      example:

          ```python
          fruits_str = "apple, banana, cherry"
          fruits = fruits_str.split(", ")
          print(fruits) # prints ["apple", "banana", "cherry"]
          ```
    - You can create a list using a list comprehension.
      
        example:
  
            ```python
            numbers = [1, 2, 3, 4, 5]
            squares = [x**2 for x in numbers]
            print(squares) # prints [1, 4, 9, 16, 25]
            ```
    - You can create a list using the `range()` function.
      
        example:
  
            ```python
            numbers = list(range(1, 6))
            print(numbers) # prints [1, 2, 3, 4, 5]
            ``` 

    - You can create a list using the `list()` function.

      example:

          ```python
          numbers = list((1, 2, 3, 4, 5))
          print(numbers) # prints [1, 2, 3, 4, 5]
          ```

    - You can create a list using the `*` operator.

      example:

          ```python
          numbers = [1, 2, 3] * 3
          print(numbers) # prints [1, 2, 3, 1, 2, 3, 1, 2, 3]
          ```
    - You can create a list using the `append()` method.
      
        example:
  
            ```python
            numbers = []
            numbers.append(1)
            numbers.append(2)
            numbers.append(3)
            print(numbers) # prints [1, 2, 3]
            ``` 

    - You can create a list using the `insert()` method.

      example:

          ```python
          numbers = [1, 3]
          numbers.insert(1, 2)
          print(numbers) # prints [1, 2, 3]
          ```
    - You can create a list using the `remove()` method.

      example:

          ```python
          numbers = [1, 2, 3]
          numbers.remove(2)
          print(numbers) # prints [1, 3]
          ```
    - You can create a list using the `pop()` method.

      example:

          ```python
          numbers = [1, 2, 3]
          numbers.pop()
          print(numbers) # prints [1, 2]
          ``` 

    - You can create a list using the `del` keyword.
      
        example:
  
            ```python
            numbers = [1, 2, 3]
            del numbers[1]
            print(numbers) # prints [1, 3]
            ```
    - You can create a list using the `clear()` method.

      example:

          ```python
          numbers = [1, 2, 3]
          numbers.clear()
          print(numbers) # prints []
          ``` 

    - You can create a list using the `copy()` method.

      example:

          ```python
          numbers = [1, 2, 3]
          numbers_copy = numbers.copy()
          print(numbers_copy) # prints [1, 2, 3]
          ``` 

    - You can create a list using the `extend()` method.

      example:

          ```python
          numbers = [1, 2, 3]
          more_numbers = [4, 5, 6]
          numbers.extend(more_numbers)
          print(numbers) # prints [1, 2, 3, 4, 5, 6]
          ```

    - You can create a list using the `reverse()` method.

      example:

          ```python
          numbers = [1, 2, 3]
          numbers.reverse()
          print(numbers) # prints [3, 2, 1]
          ``` 

    - You can create a list using the `sort()` method.


      example:

          ```python
          numbers = [3, 1, 2]
          numbers.sort()
          print(numbers) # prints [1, 2, 3]
          ```
    - sort vs sorted

      - The `sort()` method sorts the list in place, which means that it modifies the original list.

        example:

            ```python
            numbers = [3, 1, 2]
            numbers.sort()
            print(numbers) # prints [1, 2, 3]
            ```

      - The `sorted()` function returns a new sorted list without modifying the original list.

        example:

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
       example:

          ```python
          fruits = ("apple", "banana", "cherry")
          fruits_str = ", ".join(fruits)
          print(fruits_str) # prints "apple, banana, cherry"
          ```
    - string to tuple using the `split()` method.
      
        example:
  
            ```python
            fruits_str = "apple, banana, cherry"
            fruits = tuple(fruits_str.split(", "))
            print(fruits) # prints ("apple", "banana", "cherry")
            ```

- Dictionaries are unordered collections of key-value pairs, such as `{"name": "Alice", "age": 30}`, `{"a": 1, "b": 2}`, etc.

  - You can access the value of a key in a dictionary using indexing.

    example: 

        ```python
        person = {"name": "Alice", "age": 30}
        name = person["name"]
        print(name) # prints "Alice"
        ```

  - You can change the value of a key in a dictionary.
      
      example:
  
          ```python
          person = {"name": "Alice", "age": 30}
          person["age"] = 31
          print(person) # prints {"name": "Alice", "age": 31}
          ```

  - You can add a new key-value pair to a dictionary.

    example:

        ```python
        person = {"name": "Alice", "age": 30}
        person["city"] = "New York"
        print(person) # prints {"name": "Alice", "age": 30, "city": "New York"}
        ```

  - You can remove a key-value pair from a dictionary using the `pop()` method.


    example:

        ```python
        person = {"name": "Alice", "age": 30}
        person.pop("age")
        print(person) # prints {"name": "Alice"}
        ```
  - You can remove a key-value pair from a dictionary using the `del` keyword.

    example:

        ```python
        person = {"name": "Alice", "age": 30}
        del person["age"]
        print(person) # prints {"name": "Alice"}
        ```

  - You can clear a dictionary using the `clear()` method.

    example:

        ```python
        person = {"name": "Alice", "age": 30}
        person.clear()
        print(person) # prints {}
        ```

  - You can copy a dictionary using the `copy()` method.

    example:

        ```python
        person = {"name": "Alice", "age": 30}
        person_copy = person.copy()
        print(person_copy) # prints {"name": "Alice", "age": 30}
        ```

  - You can create a dictionary using the `dict()` function.

    example:

        ```python
        person = dict(name="Alice", age=30)
        print(person) # prints {"name": "Alice", "age": 30}
        ```
  - You can create a dictionary using the `fromkeys()` method.

    example:

        ```python
        keys = ["name", "age"]
        person = dict.fromkeys(keys)
        print(person) # prints {"name": None, "age": None}
        ```

  - You can create a dictionary using the `items()` method.
  
      example:
  
          ```python
          person = {"name": "Alice", "age": 30}
          items = person.items()
          print(items) # prints dict_items([("name", "Alice"), ("age", 30)])
          ```

  - You can create a dictionary using the `keys()` method.

    example:

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
     
     example:

        ```python
        x = 10
        if x > 5:
            print("x is greater than 5")
        ```

- You can use the `elif` statement to execute code if the previous condition is False.

    example:

        ```python
        x = 10
        if x > 5:
            print("x is greater than 5")
        elif x < 5:
            print("x is less than 5")
        ```

- You can use the `else` statement to execute code if all previous conditions are False.

    example:

        ```python
        x = 10
        if x > 5:
            print("x is greater than 5")
        else:
            print("x is less than or equal to 5")
        ```

- You can use the `for` statement to iterate over a sequence of items.

    example:

        ```python
        fruits = ["apple", "banana", "cherry"]
        for fruit in fruits:
            print(fruit)
        ```

- You can use the `while` statement to execute code as long as a condition is True.

    example:

        ```python
        x = 0
        while x < 5:
            print(x)
            x += 1
        ```

- You can use the `try` statement to catch exceptions in a program.

    example:

        ```python
        try:
            x = 1 / 0
        except ZeroDivisionError:
            print("Cannot divide by zero")
        ```

- You can use the `with` statement to open and close files in a program.
  
      example:
  
          ```python
          with open("file.txt", "r") as file:
              content = file.read()
              print(content)
          ```
- You can use the `assert` statement to check if an expression is True. 

    example:

        ```python
        x = 10
        assert x > 5, "x is not greater than 5"
        ```

- You can use the `yield` statement to return a value from a generator function.

    example:

        ```python
        def numbers():
            yield 1
            yield 2
            yield 3

        for number in numbers():
            print(number) # outputs 1, 2, 3
        ```

- You can use the `raise` statement to raise an exception in a program.

    example:

        ```python
        x = -1
        if x < 0:
            raise ValueError("x cannot be negative")
        ```

- You can use the `global` statement to access a global variable inside a function.

    example:

        ```python
        x = 10

        def print_x():
            global x
            print(x)

        print_x() # prints 10
        ```

- You can use the `nonlocal` statement to access a variable in the outer scope of a function.

    example:

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

        example: 

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

     example:

        ```python
        def greet():
            print("Hello, World!")

        greet() # prints Hello, World!
        ```
- You can pass arguments to a function by placing them inside the parentheses.

    example:

        ```python
        def greet(name):
            print(f"Hello, {name}!")

        greet("Alice") # prints Hello, Alice!
        ```
- You can return a value from a function using the `return` keyword.

    example:

        ```python
        def add(a, b):
            return a + b

        result = add(1, 2)
        print(result) # prints 3
        ```
- You can define default values for function arguments by using the assignment operator `=`.
  
      example:
  
          ```python
          def greet(name="World"):
              print(f"Hello, {name}!")
  
          greet() # prints Hello, World!
          greet("Alice") # prints Hello, Alice!
          ``` 

- You can pass a variable number of arguments to a function by using the `*args` and `**kwargs` syntax. 

    example:

        ```python
        def add(*args):
            return sum(args)

        result = add(1, 2, 3, 4, 5)
        print(result) # prints 15
        ``` 
    example for kwargs:
      
          ```python
          def greet(**kwargs):
              for key, value in kwargs.items():
                  print(f"{key}: {value}")
  
          greet(name="Alice", age=30) # prints name: Alice and age: 30
          ```
- You can define anonymous functions using the `lambda` keyword.  

    example:

        ```python
        add = lambda a, b: a + b
        result = add(1, 2)
        print(result) # prints 3
        ```

- You can call a function by using the function name followed by a pair of parentheses.

    example:

        ```python
        def greet():
            print("Hello, World!")

        greet() # prints Hello, World!
        ```
- You can use the `help()` function to get information about a function.
  
      example:
  
          ```python
          def greet(name):
              print(f"Hello, {name}!")
  
          help(greet)
          ```
- function parameters vs arguments
  
      - Parameters are the names used in the function definition to refer to the arguments passed to the function.
  
      - Arguments are the values passed to the function when it is called.
  
          example:
  
              ```python
              def greet(name):
                  print(f"Hello, {name}!")
  
              greet("Alice") # Alice is the argument passed to the greet function
              ```

- keyword parameters vs positional parameters

    - Positional parameters are passed to a function based on their position in the function call.
  
    - Keyword parameters are passed to a function based on their name in the function call.
  
        example:
  
            ```python
            def greet(name, age):
                print(f"Hello, {name}! You are {age} years old.")
  
            greet("Alice", 30) # Alice is the name and 30 is the age
            greet(age=30, name="Alice") # Alice is the name and 30 is the age
            ```

- default parameters
  
      - Default parameters are used to provide a default value for a parameter if no value is passed to the function.
    
          example:
    
              ```python
              def greet(name="World"):
                  print(f"Hello, {name}!")
    
              greet() # prints Hello, World!
              greet("Alice") # prints Hello, Alice!
              ```

- variable number of arguments
  
      - You can pass a variable number of arguments to a function by using the `*args` and `**kwargs` syntax.
    
          example:
    
              ```python
              def add(*args):
                  return sum(args)
    
              result = add(1, 2, 3, 4, 5)
              print(result) # prints 15
              ```
          example for kwargs:
    
              ```python

              def greet(**kwargs):
                  for key, value in kwargs.items():
                      print(f"{key}: {value}")

              greet(name="Alice", age=30) # prints name: Alice and age: 30
              ```
- anonymous functions
    
        - You can define anonymous functions using the `lambda` keyword.
      
            example:
      
                ```python
                add = lambda a, b: a + b
                result = add(1, 2)
                print(result) # prints 3
                ```   

- function scope

    - The scope of a variable refers to the region of a program where the variable is accessible.
  
    - Variables defined inside a function are local to that function and cannot be accessed outside the function.
  
    - Variables defined outside a function are global and can be accessed inside the function using the `global` keyword.
  
        example:
  
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
    
          example:
    
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
    
          example:
    
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
      
            example:
      
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
      
            example:
      
                ```python
                def add(a: int, b: int) -> int:
                    return a + b
                ```

- Function Arguments
      
          - Function arguments are the values passed to a function when it is called.
        
          - Function arguments can be passed by position or by keyword.
        
          - Function arguments can have default values.
        
          - Function arguments can be passed as a variable number of arguments using the `*args` and `**kwargs` syntax.
        
              example:
        
                  ```python
                  def greet(name):
                      print(f"Hello, {name}!")
        
                  greet("Alice") # Alice is the argument passed to the greet function
                  ```

- Function Parameters

    - Function parameters are the names used in the function definition to refer to the arguments passed to the function.
  
    - Function parameters can have default values.
  
    - Function parameters can be passed by position or by keyword.
  
        example:
  
            ```python
            def greet(name):
                print(f"Hello, {name}!")
  
            greet("Alice") # Alice is the argument passed to the greet function
            ```

### Modules


      