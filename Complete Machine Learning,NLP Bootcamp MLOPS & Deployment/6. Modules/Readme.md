### Modules

- Modules in Python means a file containing Python statements and definitions.

- A file containing Python code, for example: example.py, is called a module, and its module name would be example.

- We use modules to break down large programs into small manageable and organized files. Furthermore, modules provide reusability of code.

- We can define our most used functions in a module and import it, instead of copying their definitions into different programs.

- Let us create a module. Type the following and save it as example.py.

    ```python
    def add(a, b):
        return a + b
    ```

- We can import the module example into the Python program by using the import statement.

    ```python
    import example
    print(example.add(4, 5))
    ```

- When the above code is executed, it produces the following result.

    ```python
    9
    ```

- We can import specific names from a module without importing the module as a whole. Here is an example.

    ```python
    from example import add
    print(add(4, 5))
    ```

- When the above code is executed, it produces the following result.

    ```python
    9
    ```

- There is a built-in function to list all the function names (or variable names) in a module. The dir() function.

    ```python
    import example
    print(dir(example))
    ```

- When the above code is executed, it produces the following result.

    ```python
    ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'add']
    ```

- We can import a module by renaming it as follows.

    ```python
    import example as e
    print(e.add(4, 5))
    ```

- When the above code is executed, it produces the following result.

    ```python
    9
    ```

