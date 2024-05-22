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


