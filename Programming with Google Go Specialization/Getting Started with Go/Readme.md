### Getting Started with Go | Overview

 - Go Documentation [Official](https://go.dev/doc/#learning)

 - Why should you learn Go? 

    -  Advantages of Go:
        
        1. Code runs fast: 
        
            - Go is compiled to machine code, which makes it faster than interpreted languages like Python or Ruby.

        2. Garbage collection: 
        
            - Go has a garbage collector that automatically frees up memory that is no longer needed.
            
        3. Simpler Objects: 
        
            - Go has a simpler object model than languages like Java or C++. This makes it easier to learn and use.

        4. Concurrency is efficient: 
        
            - Go has built-in support for concurrency, which makes it easy to write programs that can do many things at once.

### Software Translation

 - Machine Language: 
 
    - The lowest level of programming language, which is the language that the computer understands. It is made up of 1s and 0s. ie CPU instructions represented in binary. eg. 01010101, 11010101, etc.

- Assembly Language:
        
    - A low-level programming language that is a more human-readable version of machine language. It uses mnemonics to represent CPU instructions. eg. ADD, SUB, MOV, etc.

- High-Level Language:
            
    - A programming language that is easier for humans to read and write than machine language or assembly language. eg. Python, Java, C++, etc.

- Compiler: 
            
    - A program that translates high-level code into machine code. It reads the entire program and translates it all at once.

- Compilation:
            
    - The process of translating high-level code into machine code, Translation occurs only once, saves time during execution. eg. C, C++, etc.

- Interpreter:

    - A program that reads high-level code and executes it line by line. It translates the code into machine code as it goes.

- Interpretation:
    
    - The process of translating high-level code into machine code line by line. Translation occurs every time the code is run, which can slow down execution. eg. Python, Ruby, etc.

    - Requires an interpreter to be installed on the computer to run the code. eg. Python, Ruby, etc.

- Efficiency vs. Ease of Use:
    
    - Compiled languages are generally faster than interpreted languages because the code is translated all at once. Interpreted languages are easier to use because they do not require a separate compilation step.

- Go is a compiled language, which means that it is translated into machine code before it is run. This makes it faster than interpreted languages like Python or Ruby. But it has some of the ease of use of an interpreted language because it has a garbage collector and built-in support for concurrency.

    - Garbage Collector: A program that automatically frees up memory that is no longer needed.

    - Where should memory be allocated? Stack or Heap?

        - Stack: 
        
            - Memory is allocated on the stack when a function is called. It is automatically freed when the function returns.

        - Heap: 
        
            - Memory is allocated on the heap when a variable is created with the `new` keyword. It is not automatically freed, so it must be freed manually.

    - When can memory be deallocated?

        - Memory can be deallocated when it is no longer needed. This can happen when a variable goes out of scope or when a program exits.

- Source Code:
    
    - The code that you write in a high-level language.

- Object Code:
    
    - The code that is output by the compiler or interpreter. It is in machine code.

- Executable:
        
    - A file that contains machine code that can be run by the computer.

- Bytecode:
        
    - An intermediate representation of the code that is used by some languages. It is not machine code, but it is not source code either. It is often used in interpreted languages like Java.

- Virtual Machine:

    - A program that runs bytecode. It simulates a computer so that the bytecode can be executed.

- Just-In-Time Compilation (JIT):

    - A technique used by some languages to improve performance. The bytecode is compiled into machine code at runtime, just before it is executed.

- Ahead-Of-Time Compilation (AOT):
    
    - A technique used by some languages to improve performance. The bytecode is compiled into machine code before it is executed.

- Cross-Compilation:
    
    - Compiling code on one type of computer so that it can be run on a different type of computer.

- Transpiler:
        
    - A program that translates code from one high-level language to another high-level language.

- All software must be translated  into the machine language that the computer understands before it can be executed.

### Object-Oriented Programming

- Object-Oriented Programming (OOP):
    
    - A programming paradigm that uses objects to represent data and methods to operate on that data.

    - Organize your code through encapsulation.

    - Group together data and functions which are related.

    - User defined type which is specific to the problem domain.

    - Go is not a pure object-oriented language, but it does support some object-oriented features.

- Object:  
        
    - An instance of a class.

- Class:
        
    - A blueprint for creating objects.

- Objects in GO | Structs and Methods:
    
    - Go does not have classes, but it does have structs.

    - A struct is a user-defined type that groups together data and functions.

    - A struct can have fields and methods.

    - Fields are data that is stored in the struct.

    - Methods are functions that operate on the data in the struct.

    - Go uses structs with associated methods to achieve object-oriented programming.

    - Simplified implementation of classes and objects.

