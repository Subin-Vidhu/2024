### Python Programming Language

- Create a new env

    - `conda create -p myenv python==3.12` # -p is the path

- Activate the environment
    
    - `conda activate myenv`

- Install ipykernel package

    - `pip install ipykernel` # This package is required to run the jupyter notebook in the new environment.


    - Use  `shift + enter` to run the code in the jupyter notebook.

- Different ways of Creating Virtual Environment

    - `python -m venv myenv`

        - To activate:
                
                - `myenv\Scripts\activate`
        
        - To check python version:
                
                - `python --version`

        - To deactivate:
                
                - `deactivate`
        

    - `virtualenv -p python3 myenv`

        - `pip install virtualenv` if not installed

        - To activate:
                
                - `myenv\Scripts\activate`
        
        - To deactivate:
                
                - `deactivate`

    - `conda create -p myenv python=3.12`

        - To activate:
                
                - `conda activate myenv`
        
        - To deactivate:
                
                - `conda deactivate`

        - some other commands:
                
            - `conda env list` # To list all the environments
            
            - `conda env remove -n myenv` # To remove the environment

        - what -p and -y and similar does?

          - `-p` is the path where the environment is created.

            - `-y` is used to skip the confirmation prompt.

            - similarly we have other flags like: 

                - `--name` or `-n` to specify the name of the environment.

                - `--file` or `-f` to specify the file containing the dependencies.

                - `--channel` or `-c` to specify the channel to install the packages from.

                - `--no-deps` to skip the installation of dependencies.

                - `--force-reinstall` to force the reinstallation of the packages.

                - `--no-pin` to not pin the dependencies.

                - `--copy` to copy the packages instead of linking them.

                - `--update-deps` to update the dependencies.

                - `--dry-run` to simulate the installation.

                - `--json` to output the result in JSON format.

                - `--all` to update all the packages.

                - `--no-update-deps` to not update the dependencies.

                - `--no-builds` to not build the packages.

- Python Basics-Syntax and Semantics

- Syntax

    - refers to the set of rules that defines the combinations of symbols that are considered to be correctly structured programs in that language ie, `the correct arrangement of words, phrases, and symbols in a program`.

- Semantics

    - refers to the meaning of the words, phrases, and symbols in a program ie the interpretation of the program, `what the code is supposed to do when it runs`.

- Basic Syntax Rules in Python

    - Python is case-sensitive ie `variable` and `Variable` are different.

        - eg: `a = 1` and `A = 2` are different.

    - Statements in Python are written in new lines ie `end of a statement is marked by a newline character`.
    
            - eg: `print("Hello World")`

    - Indentation ie `whitespace at the beginning of the line is important`.

        - eg: `if a > b:`

                - `print("a is greater than b")`
                 
                - Python uses indentation to define the block of code - ie structure and hierarchy of the code.

                - Unlike other programming languages, Python does not use braces `{}` to define the block of code

                - This means that all the statements within a block must be indented by the same amount.

    - Comments ie `#` is used to comment a single line and `'''` or `"""` is used to comment multiple lines.

        - eg: `# This is a comment`
            
            - `''' This is a multiline comment '''`

    - Multiple statements on a single line ie `semicolon` is used to separate multiple statements on a single line.

        - eg: `a = 1; b = 2; c = 3`

    - Line Continuation ie `backslash` is used to continue a statement to the next line.

        - eg: `total = 1 + 2 + 3 + \`
                
            `4 + 5 + 6`   
            print(total) # 21

    



    