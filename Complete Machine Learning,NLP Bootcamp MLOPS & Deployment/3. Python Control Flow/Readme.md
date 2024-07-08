### Python Control Flow

- If, Elif, Else

    - If statement

        - Syntax

            ```python
            if condition:
                # code block
            ```
        - Example

            ```python
            if 5 > 2:
                print("5 is greater than 2")
            ```
    
    - If else statement
    
        - Syntax

            ```python
            if condition:
                # code block
            else:
                # code block
            ```
        - Example

            ```python
            if 5 > 2:
                print("5 is greater than 2")
            else:
                print("5 is not greater than 2")
            ```

    - If elif else statement
    
        - Syntax

            ```python
            if condition:
                # code block
            elif condition:
                # code block
            else:
                # code block
            ```
        - Example

            ```python
            a = 33
            b = 33
            if b > a:
                print("b is greater than a")
            elif a == b:
                print("a and b are equal")
            else:
                print("a is greater than b")
            ```

    - Nested If

        - Syntax

            ```python
            if condition:
                # code block
                if condition:
                    # code block
            ```
        - Example

            ```python
            x = 41
            if x > 10:
                print("Above ten,")
                if x > 20:
                    print("and also above 20!")
                else:
                    print("but not above 20.")
            ```

    - For Loop

        - Syntax

            ```python
            for item in iterable:
                # code block
            ```
        - Example

            ```python
            fruits = ["apple", "banana", "cherry"]
            for x in fruits:
                print(x)
            ```
    
    - Looping Through a String

        - Syntax

            ```python
            for item in iterable:
                # code block
            ```
        - Example

            ```python
            for x in "banana":
                print(x)
            ```

    - While Loop

        - Syntax

            ```python
            while condition:
                # code block
            ```
        - Example

            ```python
            i = 1
            while i < 6:
                print(i)
                i += 1
            ```

    - Loop Control Statements

        - Break Statement

            - Syntax

                ```python
                for item in iterable:
                    # code block
                    if condition:
                        break
                ```
            - Example

                ```python
                fruits = ["apple", "banana", "cherry"]
                for x in fruits:
                    print(x) # apple, banana
                    if x == "banana":
                        break
                ```

        - Continue Statement

            - Syntax

                ```python
                for item in iterable:
                    # code block
                    if condition:
                        continue
                ```
            - Example

                ```python
                fruits = ["apple", "banana", "cherry"]
                for x in fruits: # apple, cherry
                    if x == "banana":
                        continue
                    print(x)
                ```

        - Pass Statement

            - Syntax

                ```python
                for item in iterable:
                    # code block
                    pass
                ```
            - Example

                ```python
                for x in [0, 1, 2]:
                    pass
                ```

    - Nested for loop

        - Syntax

            ```python
            for item in iterable:
                # code block
                for item in iterable:
                    # code block
            ```
        - Example

            ```python
            adj = ["red", "big", "tasty"]
            fruits = ["apple", "banana", "cherry"]
            for x in adj:
                for y in fruits:
                    print(x, y) # red apple, red banana, red cherry, big apple, big banana, big cherry, tasty apple, tasty banana, tasty cherry
            ```