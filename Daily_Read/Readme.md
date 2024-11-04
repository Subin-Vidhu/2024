# 

1. LE vs OHE
2. RAG

    ![alt text](image.png)

3. Machine Learning Build Your First AI Model with Python | [Link](https://github.com/Subin-Vidhu/2024/blob/main/Machine%20Learning%20Build%20Your%20First%20AI%20Model%20with%20Python/Class%2B11-12.ipynb)

4. Flask_Introduction | [Link](https://github.com/Subin-Vidhu/2024/tree/main/Flask_Introduction/FlaskIntroduction)

5. Linux Terminal Productivity | [Link](https://github.com/Subin-Vidhu/2024/blob/main/Linux%20Terminal%20Productivity/Linux%20Terminal%20Productivity.pdf)

    ```
    # Introduction

    commands:
    whoami
    date
    echo "hello"

    # File System

    pwd
    ls
    cd Desktop (dir name is case sensitive)
    cd ..

    cat filename
    cd ~ - automatically to home dir.

    # Find

    pwd;ls; cat filename (outputs all commands line by line.)
    find / ~name passwd (searches the whole system for password file)
    touch notes.txt (create a new file)
    find ~name *.txt (search for these files in the current dir)

    # Search in file

    wc -l /etc/passwd (word count)
    grep "hello" /files/hello.txt (search particular word)

    # Shell Operators

    ls&
    date & date
    ls > files.txt
    whoami > me.txt (creates a new txt file and outputs the answer into it)
    date » date.txt (adds to the bottom of the file)
    cat date.txt

    # Flags

    ls -l (files in list format with time and date)
    ls -a, ls —all (all files including hidden ones)
    ls —help
    man ls
    man date
    man echo
    man ssh

    # More File system

    mkdir new_folder
    rm file.txt
    cp 1.txt 2.txt
    mv 1.txt Downloads
    file 1.txt (eg: ASCII text)
    rm -R folder

    # Permissions

    su root (enter the password if prompted)
    groups
    sudo cat file.txt

    # Common directories

    etc (passwords and other config files)
    var ( variable data )
    root (home of the root user)
    tmp (temporary files, gets deleted when computer restarts)```

6. 2024 Master class on Data Science using Python A-Z for ML | [Link](https://github.com/Subin-Vidhu/2024/tree/main/2024%20Master%20class%20on%20Data%20Science%20using%20Python%20A-Z%20for%20ML)

    ```
    list.sort() - sorts the list and modifies it as well

    list2 = list1 (both the content and id same)
    list2 = list1.copy() (only the content remains the same, id differs) [to find id = id(list)]

    tuple1 = 1,2,3 [Any comma-separated sequence of values defines a tuple]

    dict.get(key) - returns none if no value exists

    function exists as soon as the return statement is called. (define - parameters [DP], function_call - arguments [CA])

    Flatten matrix [transform a matrix to a one dimensional numpy array]
    a
    Out: 
    array([[1, 2, 3],
            [4, 5, 6]])
    
    a.flatten()
    Out: array([1, 2, 3, 4, 5, 6])

    ```