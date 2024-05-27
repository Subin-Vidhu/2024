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
    
    - Go does not have classes, but it does have `structs`.

    - A struct is a user-defined type that groups together data and functions.

    - A struct can have fields and methods.

    - Fields are data that is stored in the struct.

    - Methods are functions that operate on the data in the struct.

    - Go uses structs with associated methods to achieve object-oriented programming.

    - Simplified implementation of classes and objects.

### Concurrency

 - Performance Limits:
    
    - Moore's Law used to be a guideline for the performance of computers. It stated that the number of transistors on a chip would double every 18 months.

    - More transistors on a chip meant more processing power ie higher clock frequency.

    - But the clock frequency has not increased significantly in recent years. Power/temperature constraints have limited the clock frequency.

    - Performance improvements are now achieved through parallelism.

- Parallelism:
    
    - Number of cores still increases with each new generation of processors.

    - Running multiple tasks at the same time on different cores.

    - Can be achieved through multi-core processors.

    - Difficulties with parallelism:

        - When do tasks start/stop?
        - What if one task needs data from another task?
        - How do tasks communicate?
        - Do tasks conflict in memory access?

- Concurrency:

    - Managing multiple tasks at the same time.

    - A way to structure a program so that it can run multiple tasks at the same time.

    - Concurrent programming enables parallelism:

        - Management of task execution.
        - Communication between tasks.
        - Synchronization of tasks.

    - Tasks are called `goroutines` in Go.

    - Goroutines are lightweight threads that are managed by the Go runtime.

    - Goroutines are started with the `go` keyword.

    - `Channels` are used to communicate between goroutines.

    - Channels are a type in Go that can be used to send and receive data between goroutines.

    - `Select` enables task synchronization.


### Installing GO

- Download the Go installer from the official website [here](https://golang.org/dl/)

### Workspaces and Packages

- Go uses workspaces to organize your code.

    - A workspace is a directory that contains your Go code.
    - Hierarchy of directories:
        - `src` directory: Contains your Go source code files.
        - `pkg` directory: Contains package objects.
        - `bin` directory: Contains executable files.
    - Programmer typically has one workspace for many projects.
    - Directory hierarchy is recommended not enforced.
    
    - Workspace directroy is set by the `GOPATH` environment variable.

- Packages:

    - Group of related source files.
    - Each package has a unique name.
    - Each package can be imported by other packages.
    - Enables software reuse.
    - First line of file names the package. eg. `package main`
        - `main` package is used to create an executable.

    - Importing Packages:
        - `import "fmt"` imports the `fmt` package.
        - `import "math/rand"` imports the `rand` package from the `math` package.

    - Package Naming:

        - Package name is the last element of the import path.
        - `import "math/rand"` imports the `rand` package from the `math` package.
        - `import "github.com/golang/example/hello"` imports the `hello` package from the `github.com/golang/example` package.

    - Package Main
    
        - The `main` package is used to create an executable.
        - The `main` function is the entry point of the program.
        - The `main` function is called when the program is run.
        eg. 
        
        ```go
        package main
        import "fmt"
        func main() { 
            fmt.Printf("Hello World!\n") }
        ```

### Go Tools

- Go has a set of tools that help you write, build, and run Go code, ie manage GO source code.

    - `import': access other packages.
        - `fmt`: format code.
        - Searches directories specified by GOROOT and GOPATH environment variables.

    - `go build`: Compiles the code in the current directory.
        - eg. `go build hello.go` compiles the `hello.go` file.
    - `go run`: Compiles and runs the code in the current directory, tie compiles .go files and runs the executable.
        - eg. `go run hello.go` runs the `hello.go` file.
    - `go test`: Runs tests in the current directory.
    - `go fmt`: Formats the code in the current directory.
    - `go get`: Downloads and installs packages.
    - `go doc`: Displays documentation for a package.
    - `go vet`: Reports suspicious constructs in the code.
    - `go generate`: Generates Go files by processing source files.
    - `go list`: Lists the packages in the current directory.

### Go Variables

- Variables are used to store data in a program.

- It should have a name and a type.

- Variable Declaration:
    - `var name type = value`
    - `var name = value`
    - `name := value`

- Variable Types:

    - `int`: Integer
    - `float64`: Floating-point number
    - `bool`: Boolean
    - `string`: String
    - `byte`: Byte
    - `rune`: Unicode character
    - `complex64`: Complex number with float32 real and imaginary parts
    - `complex128`: Complex number with float64 real and imaginary parts

- Constants:
    
    - Constants are variables whose values cannot be changed.
    - Declared using the `const` keyword.
    - `const name = value`

- Multiple Variables:

    - Multiple variables can be declared on the same line.
    - `var name1, name2 type = value1, value2`
    - `var name1, name2 = value1, value2`
    - `name1, name2 := value1, value2`

- Zero Values:

    - Variables that are declared but not initialized are set to their zero values.
    - `int`: 0
    - `float64`: 0.0
    - `bool`: false
    - `string`: ""
    - `byte`: 0
    - `rune`: 0
    - `complex64`: 0 + 0i
    - `complex128`: 0 + 0i

- Type Conversion:
    
    - Variables can be converted from one type to another.
    - `var name type = type(value)`

- Short Variable Declaration:
        
    - Variables can be declared and initialized on the same line.
    - `name := value`

### Variable Initialization

- Variables can be initialized when they are declared.

- Variable Initialization:
    - `var name type = value`
    - `var name = value`
    - `name := value`

- Unintialized Variables:
    - Variables that are declared but not initialized are set to their zero values.
    - `int`: 0
    - `float64`: 0.0
    - `bool`: false
    - `string`: ""
    - `byte`: 0
    - `rune`: 0
    - `complex64`: 0 + 0i
    - `complex128`: 0 + 0i

- Variables can be initialized in the declaration statement or later in the program.eg.

```go  
package main
import "fmt"
func main() {
    var name string
    name = "John"
    fmt.Println(name)
}
```

- Variables can be initialized with a value when they are declared. eg.

```go   
package main
import "fmt"
func main() {
    var name string = "John"
    fmt.Println(name)
}
```
### Pointers

- Pointers are variables that store the memory address of another variable ie an address to data in memory.

- & operator returns memory address of a variable/function.

- * operator returns the data at the memory address.

- eg. 

    ```go
    var x int = 10
    var y int
    var ip *int // pointer to an integer
    ip = &x // store the address of x in ip
    y = *ip // store the value at the address in y
    fmt.Println(*y)
    ```

- New
    
    - The `new` function returns a pointer to a newly allocated zero value of the specified type.

    - new() creates a variable and returns a pointer to the variable.

    - eg. `p := new(int)` creates a pointer to an integer.

### Variable Scope

- The places in the code where a variable can be accessed.

- Variables can be declared at the package level or the function level.

- Package-level variables can be accessed by any function in the package.

- Function-level variables can only be accessed by the function in which they are declared.

- Blocks

    - A block is a group of statements enclosed in curly braces.

    - Variables declared in a block are only accessible within that block.

    - Variables declared in a block are not accessible outside the block.

        - eg
            
            ```go
            package main
            import "fmt"
            func main() {
                x := 10
                if x > 5 {
                    y := 20
                    fmt.Println(y)
                }
                fmt.Println(x)
            }
            ```

- Lexical Scoping

    - The scope of a variable is determined by its location in the code.

    - Variable accessible form block bj if :
    
        - Variable is declared in block bi.
        - bi >= bj.

### Deallocating Memory

- When a variable is no longer needed, it should be deallocated, otherwise, it will run out of memory.

- Go has a garbage collector that automatically frees up memory that is no longer needed.

- Stack vs. Heap

    - Memory is allocated on the stack when a function is called. It is automatically freed when the function returns.

    - Memory is allocated on the heap when a variable is created with the `new` keyword. It is not automatically freed, so it must be freed manually.

### Garbage Collection

- Go has a garbage collector that automatically frees up memory that is no longer needed.

- Pointers and Deallocation
    
    - Go has a garbage collector that automatically frees up memory that is no longer needed.

    - Memory is deallocated when it is no longer needed.

    - Memory can be deallocated when a variable goes out of scope or when a program exits.

    - Hard to determine when a variable is no longer needed.
        eg. 

        ```go 
        func foo() * int{
            x := 10
            return &x
        }

        func main() {
            var y *int
            y := foo()
            fmt.Println(*y)
        }
        ``` 
- In interpreted languages, garbage collection is done by the interpreter, eg. for python the python interpreter, for java the JVM.

    - easy for the programmer, but can slow down execution.

- But when it comes to Go, GO is a coompiled language which enables garbage collection.

    - implementation is fast
    - compiler determines stack vs heap allocation
    - garbage collection is done by the Go runtime in the background.

### Comments

- Comments are used to document code.

- Single-line comments start with `//`.

- Multi-line comments start with `/*` and end with `*/`.

- Comments are ignored by the compiler.

    - eg. 
    
        ```go
        // This is a single-line comment
        /* This is a
        multi-line comment */
        ```

### Print Statements

- Print statements are used to display output.

    -Improt form the fmt package
    - `fmt.Println()` prints a new line after the output.
    - `fmt.Print()` does not print a new line after the output.
    - `fmt.Printf()` prints formatted output.
        - eg. 
        
            ```go
            name := "John"
            fmt.Printf("Hello, %s!\n", name)
            ```

    - `fmt.Sprintf()` returns a formatted string.


### Integers

- Integers are whole numbers.

- Integers can be signed or unsigned.

- Different lengths and signs of integers are used for different purposes. eg. `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`.

- Binary, Octal, and Hexadecimal

    - Binary: `0b` or `0B` prefix.
    - Octal: `0` prefix.
    - Hexadecimal: `0x` or `0X` prefix.

- Binary Operators

    - `+`: Addition
    - `-`: Subtraction
    - `*`: Multiplication
    - `/`: Division
    - `%`: Modulus
    - `++`: Increment
    - `--`: Decrement

- Bitwise Operators

    - `&`: Bitwise AND
    - `|`: Bitwise OR
    - `^`: Bitwise XOR
    - `<<`: Bitwise left shift
    - `>>`: Bitwise right shift
    - `&^`: Bit clear

### Floating-Point Numbers

- Floating-point numbers are numbers with a decimal point.

- Floating-point numbers can be signed or unsigned.

- Different lengths and signs of floating-point numbers are used for different purposes. eg. `float32`, `float64`.

- Floating-Point Operators

    - `+`: Addition
    - `-`: Subtraction
    - `*`: Multiplication
    - `/`: Division

- Comparison Operators
    
    - `==`: Equal to
    - `!=`: Not equal to
    - `<`: Less than
    - `>`: Greater than
    - `<=`: Less than or equal to
    - `>=`: Greater than or equal to

### ASCII and Unicode

- ASCII

    - American Standard Code for Information Interchange.

    - 7-bit character encoding standard, each character is associated with an 8-bit number.

    - 128 characters: 0-127.

    - eg. `A` is 0x41, `a` is 0x61.

- Unicode
    
    - Character encoding standard that supports multiple languages.

    - 32-bit character encoding standard.

    - UTF-8, UTF-16, UTF-32.

        -  UTF-8 are same as ASCII for the first 128 characters.

        -  UTF-16 uses 16 bits for most characters.

        -  UTF-32 uses 32 bits for all characters.

    - Code points: Unique numbers assigned to each character.

    - Rune: a codepoint in Go.

### Strings

- Strings are sequences of characters.

- Strings are immutable.

- Strings can be concatenated with the `+` operator.

- Strings can be compared with the `==` operator.

- Strings can be indexed with the `[]` operator.

- Strings can be sliced with the `[:]` operator.

- Strings can be converted to bytes with the `[]byte()` function.

- Strings can be converted to runes with the `[]rune()` function.

- Strings can be formatted with the `fmt.Sprintf()` function.

- strconv package can be used to convert strings to other types.

    - eg. `strconv.Atoi()` converts a string to an integer.
        ```go
        package main
        import (
            "fmt"
            "strconv"
        )
        func main() {
            s := "10"
            i, _ := strconv.Atoi(s)
            fmt.Println(i)
        }
        ```

    - eg. `strconv.ParseFloat()` converts a string to a float.
    - eg. `strconv.Itoa()` converts an integer to a string.

        - eg. 
        
            ```go
            package main
            import (
                "fmt"
                "strconv"
            )
            func main() {
                i := 10
                s := strconv.Itoa(i)
                fmt.Println(s)
            }
            ```
    
### Constants

- Constants are variables whose values cannot be changed.

- Constants must be different but actual values is not important.

- iota is a special constant that is used to create a sequence of related constants.

    - eg. 
    
        ```go
        package main
        import "fmt"
        const (
            A = iota
            B
            C
        )
        func main() {
            fmt.Println(A, B, C)
        }
        ```