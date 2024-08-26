'''
Multiprocessing
Multiprocessing is a technique where multiple processes can execute concurrently. In Python, each process has its own memory space and can execute independently.

Advantages:

CPU-bound tasks: Multiprocessing is suitable for CPU-bound tasks like scientific computing, data compression, or image processing.
Independent: Processes are independent and not affected by the GIL.
True parallelism: Multiprocessing can achieve true parallelism, where multiple processes can execute simultaneously.
Disadvantages:

Heavyweight: Processes are slower to create and switch between compared to threads.
Communication overhead: Processes have their own memory space, which can make communication between them more complex.
'''

import multiprocessing
import time

def print_numbers():
    for i in range(10):
        time.sleep(1)
        print(i)

def print_letters():
    for letter in 'abcdefghij':
        time.sleep(1)
        print(letter)

if __name__ == '__main__':
    # Create processes
    process1 = multiprocessing.Process(target=print_numbers)
    process2 = multiprocessing.Process(target=print_letters)

    # Start processes
    process1.start()
    process2.start()

    # Wait for processes to finish
    process1.join()
    process2.join()