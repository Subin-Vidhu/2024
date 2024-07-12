### File Handling in Python

- File handling is an important part of any web application.

- Python has several functions for creating, reading, updating, and deleting files.

- The key function for working with files in Python is the open() function.

- The open() function takes two parameters; filename, and mode.

- There are four different methods (modes) for opening a file:

    - "r" - Read - Default value. Opens a file for reading, error if the file does not exist

    - "a" - Append - Opens a file for appending, creates the file if it does not exist

    - "w" - Write - Opens a file for writing, creates the file if it does not exist

    - "x" - Create - Creates the specified file, returns an error if the file exists

- In addition you can specify if the file should be handled as binary or text mode

    - "t" - Text - Default value. Text mode

    - "b" - Binary - Binary mode (e.g. images)

- Syntax

    ```python
    f = open("demofile.txt")
    ```

    - The above code opens the file in read mode.

    - To open the file, use the built-in open() function.

    - The open() function returns a file object, which has a read() method for reading the content of the file.

    - The file can be opened in binary mode by adding 'b' to the mode.

    - The file can be opened in append mode by adding 'a' to the mode.

    - The file can be opened in write mode by adding 'w' to the mode.

    - The file can be opened in create mode by adding 'x' to the mode.

- Example

    ```python
    f = open("demofile.txt", "rt") # Opens the file in read mode, rt stands for read text
    ```

- File Methods

    - There are different file methods available in Python.

    - Some of the methods are:

        - read() - Returns the content of the file

        - read(n) - Returns n characters from the file

        - readline() - Returns one line from the file

        - readlines() - Returns a list of lines from the file

        - write() - Writes the specified string to the file

        - writelines() - Writes a list of strings to the file

    - Example

        ```python
        f = open("demofile.txt", "r")
        print(f.read())
        ```

- Close Files

    - It is a good practice to always close the file when you are done with it.

    - Syntax

        ```python
        f = open("demofile.txt", "r")
        print(f.read())
        f.close()
        ```

    - The above code closes the file after reading it.

- Write to an Existing File

    - To write to an existing file, you must add a parameter to the open() function:

        - "a" - Append - will append to the end of the file

        - "w" - Write - will overwrite any existing content

    - Example

        ```python
        f = open("demofile.txt", "a")
        f.write("Now the file has more content!")
        f.close()
        ```

- Create a New File

    - To create a new file in Python, use the open() method, with one of the following parameters:

        - "x" - Create - will create a file, returns an error if the file exist

        - "a" - Append - will create a file if the specified file does not exist

        - "w" - Write - will create a file if the specified file does not exist

    - Example

        ```python
        f = open("myfile.txt", "x")
        ```

- Delete a File

    - To delete a file, you must import the OS module, and run its os.remove() function:

    - Example

        ```python
        import os
        os.remove("demofile.txt")
        ```


- Check if File exist

    - To avoid getting an error, you might want to check if the file exists before you try to delete it:

    - Example

        ```python
        import os
        if os.path.exists("demofile.txt"):
            os.remove("demofile.txt")
        else:
            print("The file does not exist")
        ```

- Delete Folder

    - To delete an entire folder, use the os.rmdir() method:

    - Example

        ```python
        import os
        os.rmdir("myfolder")
        ```

- Check if Folder exist

    - To avoid getting an error, you might want to check if the folder exists before you try to delete it:

    - Example

        ```python
        import os
        if os.path.exists("myfolder"):
            os.rmdir("myfolder")
        else:
            print("The folder does not exist")
        ```

- File Handling in Python

    - using with statement

    - The best way to close a file is by using the with statement. This ensures that the file is properly closed after its suite finishes, even if an exception is raised on the way.

    - It is a good practice to use the with keyword when dealing with file objects. The advantage is that the file is properly closed after its suite finishes, even if an exception is raised at some point.

    - Syntax

        ```python
        with open("demofile.txt") as f:
            print(f.read())
        ```



