### Functions

- **Functions** are a block of code that only runs when it is called. You can pass data, known as parameters, into a function. A function can return data as a result.

- **Syntax**:
    ```python
    def function_name(parameters):
        # code
        return value
    ```

- **Types of Functions**:

    - **Built-in Functions**: Functions that are built into Python.

        - **Lambda Functions**: Anonymous functions that are defined using the `lambda` keyword.  

            - **Syntax**:
                ```python
                lambda arguments: expression
                ```
            - **Example**:
                ```python
                add = lambda x, y: x + y
                print(add(5, 3)) # 8
                ```

        - **Recursive Functions**: Functions that call themselves.

            - **Example**:
                ```python
                def factorial(n):
                    if n == 0:
                        return 1
                    else:
                        return n * factorial(n-1)
                print(factorial(5)) # 120
                ```

        - **Higher-order Functions**: Functions that take other functions as arguments or return them.

            - **Example**:
                ```python
                def apply(func, x, y):
                    return func(x, y)
                def add(x, y):
                    return x + y
                print(apply(add, 5, 3)) # 8
                ```

        - **Anonymous Functions**: Functions that are defined without a name using the `lambda` keyword.
            
            - **Example**:
                ```python
                add = lambda x, y: x + y
                print(add(5, 3)) # 8
                ```


        - **Nested Functions**: Functions defined inside another function.

            - **Example**:
                ```python
                def outer_function():
                    def inner_function():
                        print("Inside Inner Function")
                    print("Inside Outer Function")
                    inner_function()
                outer_function()
                ```

        - **Partial Functions**: Functions that are used to fix a certain number of arguments of a function and generate a new function.

            - **Example**:
                ```python
                from functools import partial
                def add(x, y):
                    return x + y
                add_five = partial(add, 5)
                print(add_five(3)) # 8
                ```

        - **Generator Functions**: Functions that return an iterator.

            - **Example**:
                ```python
                def square_numbers(n):
                    for i in range(n):
                        yield i**2
                for num in square_numbers(5):
                    print(num)
                ```

        - **Decorators**: Functions that modify the functionality of another function.

            - **Example**:
                ```python
                def decorator_function(func):
                    def wrapper():
                        print("Before Function Execution")
                        func()
                        print("After Function Execution")
                    return wrapper
                @decorator_function
                def say_hello():
                    print("Hello")
                say_hello()
                ```

        - **Closures**: Functions that return a function.

            - **Example**:
                ```python
                def outer_function(message):
                    def inner_function():
                        print(message)
                    return inner_function
                my_func = outer_function("Hello")
                my_func() # Hello
                ```


        - **filter() Function**: Used to filter the given iterable with the help of another function passed as an argument to test all the elements to be True or False.

            - **Syntax**:
                ```python
                filter(function, iterable)
                ```
            - **Example**:
                ```python
                def is_even(n):
                    return n % 2 == 0
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                even_numbers = list(filter(is_even, numbers))
                print(even_numbers) # [2, 4, 6, 8, 10]
                ```

        - **map() Function**: Applies a given function to all the iterables and returns a new list.

            - **Syntax**:
                ```python
                map(function, iterable)
                ```
            - **Example**:
                ```python
                def square(n):
                    return n**2
                numbers = [1, 2, 3, 4, 5]
                squared_numbers = list(map(square, numbers))
                print(squared_numbers) # [1, 4, 9, 16, 25]
                ```

        - **reduce() Function**: Applies a function to the elements of an iterable cumulatively.

            - **Syntax**:
                ```python
                reduce(function, iterable)
                ```
            - **Example**:
                ```python
                from functools import reduce
                def add(x, y):
                    return x + y
                numbers = [1, 2, 3, 4, 5]
                sum = reduce(add, numbers)
                print(sum) # 15
                ```
        - **zip() Function**: Returns an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together, etc.

            - **Syntax**:
                ```python
                zip(iterable1, iterable2, ...)
                ```
            - **Example**:
                ```python
                names = ["Alice", "Bob", "Charlie"]
                ages = [24, 30, 28]
                for name, age in zip(names, ages):
                    print(f"{name} is {age} years old")
                ```

        - **enumerate() Function**: Adds a counter to an iterable and returns it in a form of an enumerate object.

            - **Syntax**:
                ```python
                enumerate(iterable, start=0)
                ```
            - **Example**:
                ```python
                names = ["Alice", "Bob", "Charlie"]
                for index, name in enumerate(names):
                    print(f"{index}: {name}") # 0: Alice, 1: Bob, 2: Charlie
                ```

        - **all() Function**: Returns True if all elements of the iterable are true.

            - **Syntax**:
                ```python
                all(iterable)
                ```
            - **Example**:
                ```python
                numbers = [1, 2, 3, 4, 5]
                print(all(numbers)) # True
                ```

        - **any() Function**: Returns True if any element of the iterable is true.
                
                - **Syntax**:
                    ```python
                    any(iterable)
                    ```
                - **Example**:
                    ```python
                    numbers = [0, 0, 0, 0, 1]
                    print(any(numbers)) # True
                    ```
        - **sorted() Function**: Returns a new sorted list from the elements of any iterable.

            - **Syntax**:
                ```python
                sorted(iterable, key=None, reverse=False)
                ```
            - **Example**:
                ```python
                numbers = [5, 2, 3, 1, 4]
                sorted_numbers = sorted(numbers)
                print(sorted_numbers) # [1, 2, 3, 4, 5]
                ```
        - **sum() Function**: Returns the sum of all the elements in the iterable.

            - **Syntax**:
                ```python
                sum(iterable, start=0)
                ```
            - **Example**:
                ```python
                numbers = [1, 2, 3, 4, 5]
                print(sum(numbers)) # 15
                ```
        - **len() Function**: Returns the length of the iterable.

            - **Syntax**:
                ```python
                len(iterable)
                ```
            - **Example**:
                ```python
                numbers = [1, 2, 3, 4, 5]
                print(len(numbers)) # 5
                ```

        - **max() Function**: Returns the largest element in the iterable.

            - **Syntax**:
                ```python
                max(iterable, key=None)
                ```
            - **Example**:
                ```python
                numbers = [1, 2, 3, 4, 5]
                print(max(numbers)) # 5
                ```
        -  **min() Function**: Returns the smallest element in the iterable.

            - **Syntax**:
                ```python
                min(iterable, key=None)
                ```
            - **Example**:
                ```python
                numbers = [1, 2, 3, 4, 5]
                print(min(numbers)) # 1
                ```
        - **abs() Function**: Returns the absolute value of a number.

            - **Syntax**:
                ```python
                abs(number)
                ```
            - **Example**:
                ```python
                print(abs(-5)) # 5
                ```
        - **round() Function**: Returns the rounded value of a number.

            - **Syntax**:
                ```python
                round(number, ndigits=None)
                ```
            - **Example**:
                ```python
                print(round(3.14159, 2)) # 3.14
                ```
        - **pow() Function**: Returns the value of x to the power of y.

            - **Syntax**:
                ```python
                pow(x, y, z=None)
                ```
            - **Example**:
                ```python
                print(pow(2, 3)) # 8
                ```

        - **dir() Function**: Returns a list of valid attributes of the object.

            - **Syntax**:
                ```python
                dir(object)
                ```
            - **Example**:
                ```python
                print(dir(list)) # ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter

        - **help() Function**: Returns the documentation of the object.

            - **Syntax**:
                ```python
                help(object)
                ```
            - **Example**:
                ```python
                print(help(list))
                ```

        - **type() Function**: Returns the type of the object.

            - **Syntax**:
                ```python
                type(object)
                ```
            - **Example**:
                ```python
                print(type(5)) # <class 'int'>
                ```
        - **id() Function**: Returns the unique id of the object.
        
            - **Syntax**:
                ```python
                id(object)
                ```
            - **Example**:
                ```python
                print(id(5)) # 140732674004192
                ```

        - **isinstance() Function**: Returns True if the object is an instance of the class.

            - **Syntax**:
                ```python
                isinstance(object, class)
                ```
            - **Example**:
                ```python
                print(isinstance(5, int)) # True
                ```
        - **issubclass() Function**: Returns True if the object is a subclass of the class.

            - **Syntax**:
                ```python
                issubclass(class, classinfo)
                ```
            - **Example**:
                ```python
                print(issubclass(int, object)) # True
                ```

    - **User-defined Functions**: Functions defined by the users themselves.

        - **Example**:
            ```python
            def greet(name):
                print(f"Hello, {name}")
            greet("Alice") # Hello, Alice
            ```
    - **Arguments**:

        - **Default Arguments**: Arguments that take a default value if no argument value is passed during the function call.

            - **Example**:
                ```python
                def greet(name="Alice"):
                    print(f"Hello, {name}")
                greet() # Hello, Alice
                ```

    - **Keyword Arguments**: Arguments preceded by an identifier when we pass them to a function.

        - **Example**:
            ```python
            def greet(name):
                print(f"Hello, {name}")
            greet(name="Alice") # Hello, Alice
            ```

    - **Arbitrary Arguments**: Arguments that allow us to pass a variable number of arguments to a function.

        - **Example**:
            ```python
            def greet(*names):
                for name in names:
                    print(f"Hello, {name}")
            greet("Alice", "Bob", "Charlie")
            ```

    - **Arbitrary Keyword Arguments**: Arguments that allow us to pass a variable number of keyword arguments to a function.

        - **Example**:
            ```python
            def greet(**names):
                for name, value in names.items():
                    print(f"{name}: {value}")
            greet(name1="Alice", name2="Bob", name3="Charlie")
            ```

    - **Unpacking Arguments**: Allows us to unpack the values in an iterable such as a list or tuple into the arguments of a function.

        - **Example**:
            ```python
            def greet(name1, name2, name3):
                print(f"Hello, {name1}, {name2}, {name3}")
            names = ["Alice", "Bob", "Charlie"]
            greet(*names)
            ```

    

