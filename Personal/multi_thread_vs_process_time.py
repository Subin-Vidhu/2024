import threading
import multiprocessing
import time

def print_numbers():
    for i in range(1, 11):
        time.sleep(1)
        print(i)

def print_letters():
    for letter in 'abcdefghij':
        time.sleep(1)
        print(letter)

def multithreading_example():
    start_time = time.time()

    # Create threads
    thread1 = threading.Thread(target=print_numbers)
    thread2 = threading.Thread(target=print_letters)

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for threads to finish
    thread1.join()
    thread2.join()

    end_time = time.time()
    print(f"Multithreading time taken: {end_time - start_time} seconds")

def multiprocessing_example():
    start_time = time.time()

    # Create processes
    process1 = multiprocessing.Process(target=print_numbers)
    process2 = multiprocessing.Process(target=print_letters)

    # Start processes
    process1.start()
    process2.start()

    # Wait for processes to finish
    process1.join()
    process2.join()

    end_time = time.time()
    print(f"Multiprocessing time taken: {end_time - start_time} seconds")

if __name__ == '__main__':
    # Run multithreading example
    print("Multithreading example:")
    multithreading_example()

    # Run multiprocessing example
    print("\nMultiprocessing example:")
    multiprocessing_example()