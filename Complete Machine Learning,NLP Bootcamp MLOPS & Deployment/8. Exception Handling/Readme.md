### Exception Handling

- is a mechanism to handle runtime errors. It is mainly used to handle the checked exceptions. If an exception occurs in the program, the rest of the code will not execute. So, it is recommended to handle the exception.

- Python provides a way to handle the exceptions so that the code can be executed without any interruption. The code that might cause an exception is placed in the try block. The code that handles the exception is written in the except block.

- The try block is used to check some code for errors. The code inside the try block will execute when there is no error in the program. If any error occurs, the code inside the except block will execute.

- The except block is used to handle the exception. It is used to catch and handle the exception.

- The finally block is used to execute the code whether an exception is handled or not.

- The else block is used to execute the code if the try block does not raise an exception.

- The raise keyword is used to raise an exception.

- The assert keyword is used to check if the given expression is true or false. If the expression is true, the program will continue execution. If the expression is false, the program will raise an AssertionError.

- python codes for the above are as follows:
    
    ```python
    try:
        # code that might raise an exception
    except ExceptionName:
        # code that handles the exception
    finally:
        # code that will execute whether an exception is handled or not
    else:
        # code that will execute if the try block does not raise an exception

    raise ExceptionName("message")

    assert expression
    ```

- Example:

    ```python   
    try:
        a = 10 / 0
    except ZeroDivisionError:
        print("Division by zero")
    else:
        print("No exception")
    finally:
        print("Finally block")
    ```

- When the above code is executed, it produces the following result.

    ```python
    Division by zero
    Finally block
    ```

- all examples:

    ```python
    # try-except block
    try:
        a = 10 / 0
    except ZeroDivisionError:
        print("Division by zero")
    else:
        print("No exception")
    finally:
        print("Finally block")

    # raise an exception
    try:
        raise ZeroDivisionError("Divide by zero")
    except ZeroDivisionError:
        print("Division by zero")
    finally:
        print("Finally block")
    
    # assert statement
    a = 10
    assert a > 10
    print("Assertion passed") # AssertionError
    ```

