# Python Utility Functions

This repository contains a collection of Python utility functions demonstrating various programming concepts and practical applications. Each module is explained in detail below, including its purpose, working principles, and implementation details.

## Table of Contents

1. [String Formatter](#1-string-formatter)
2. [Temperature Converter](#2-temperature-converter)
3. [Fibonacci Sequence](#3-fibonacci-sequence)
4. [Prime Number Check](#4-prime-number-check)
5. [Multi-threaded File Downloader](#5-multi-threaded-file-downloader)
6. [Testing](#6-testing)

## 1. String Formatter

### Purpose
The String Formatter module provides functionality to change the case of strings.

### Working Principles
- `format_string(s, flag)`: 
  - Takes a string `s` and a boolean `flag` as input.
  - If `flag` is True, it converts the entire string to uppercase using the `upper()` method.
  - If `flag` is False, it converts the entire string to lowercase using the `lower()` method.
  - This function demonstrates the use of a ternary operator in Python.

- `print_formatted(strings, flag)`:
  - Takes a list of strings and a boolean flag.
  - Iterates through each string in the list.
  - Calls `format_string()` for each string and prints the result.
  - This function shows how to apply a function to elements of a list.

### Implementation Details
- Uses built-in string methods `upper()` and `lower()`.
- Demonstrates list iteration and function application.

## 2. Temperature Converter

### Purpose
This module converts temperatures between Celsius and Fahrenheit scales.

### Working Principles
- `celsius_to_fahrenheit(celsius)`:
  - Implements the formula: °F = (°C × 9/5) + 32
  - Rounds the result to two decimal places for precision.

- `fahrenheit_to_celsius(fahrenheit)`:
  - Implements the formula: °C = (°F - 32) × 5/9
  - Rounds the result to two decimal places.

- `convert_temperatures(temperatures, direction)`:
  - Takes a list of temperatures and a conversion direction ('CtoF' or 'FtoC').
  - Uses list comprehension to apply the appropriate conversion function to each temperature.
  - Raises a `ValueError` if an invalid direction is provided.

### Implementation Details
- Uses mathematical operations and rounding.
- Demonstrates list comprehension and error handling.

## 3. Fibonacci Sequence

### Purpose
Calculates Fibonacci numbers efficiently.

### Working Principles
- `fibonacci(n)`:
  - Implements an iterative approach to calculate the nth Fibonacci number.
  - Handles base cases (n = 0 and n = 1) separately.
  - For n > 1, uses a loop to calculate Fibonacci numbers up to the nth term.
  - Uses variable swapping to maintain only the last two Fibonacci numbers in memory.

### Implementation Details
- Efficient iterative implementation avoiding recursion.
- Demonstrates loop usage and variable swapping.
- Includes input validation to ensure n is non-negative.

## 4. Prime Number Check

### Purpose
Determines whether a given number is prime.

### Working Principles
- `is_prime(n)`:
  - Implements an optimized algorithm to check for primality.
  - Handles base cases: numbers less than or equal to 1 are not prime.
  - Checks divisibility only up to the square root of n, optimizing the process.
  - Returns True if no divisors are found, False otherwise.

### Implementation Details
- Uses mathematical optimization to reduce the number of checks.
- Demonstrates efficient algorithm design for a common mathematical problem.

## 5. Multi-threaded File Downloader

### Purpose
Downloads multiple files concurrently to improve efficiency.

### Working Principles
- `download_file(url, destination)`:
  - Creates the destination directory if it doesn't exist.
  - Uses the `requests` library to download the file content.
  - Writes the content to the specified destination.
  - Includes error handling for network and file operations.

- `download_files_concurrently(urls, destinations)`:
  - Takes lists of URLs and corresponding destination paths.
  - Creates a separate thread for each download operation.
  - Starts all threads and then waits for them to complete.

### Implementation Details
- Uses the `threading` module for concurrent operations.
- Demonstrates file I/O, network operations, and error handling.
- Shows how to use threads to improve performance in I/O-bound tasks.

## 6. Testing

### Purpose
Ensures the correctness of all implemented functions.

### Working Principles
Each module has a corresponding test function:
- `test_string_formatter()`: Tests various string formatting scenarios.
- `test_temperature_converter()`: Checks temperature conversions for accuracy.
- `test_fibonacci()`: Verifies Fibonacci number calculations for different inputs.
- `test_prime_check()`: Tests prime number identification for various cases.
- `test_file_downloader()`: Validates concurrent file downloading functionality.

### Implementation Details
- Uses assert statements to check function outputs against expected results.
- For the file downloader, checks file existence and non-zero size after download.

## Usage

To run all tests, execute the script:

```python
python script_name.py