'''
Multithreading
Multithreading is a technique where a single process can execute multiple threads concurrently. In Python, threads are lightweight and share the same memory space.

Advantages:

Lightweight: Threads are faster to create and switch between compared to processes.
Shared Memory: Threads can share data and communicate with each other easily.
IO-bound tasks: Multithreading is suitable for IO-bound tasks like making API calls, reading files, or interacting with databases.
Disadvantages:

Global Interpreter Lock (GIL): The GIL prevents multiple threads from executing Python bytecodes at the same time. This can limit the performance of CPU-bound tasks.
Limited control: Threads are not as independent as processes and can be affected by the GIL.
'''
import threading
import time

def print_numbers():
    for i in range(10):
        time.sleep(1)
        print(i)

def print_letters():
    for letter in 'abcdefghij':
        time.sleep(1)
        print(letter)

# Create threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Start threads
thread1.start()
thread2.start()

# Wait for threads to finish
thread1.join()
thread2.join()