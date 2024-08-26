import threading
import multiprocessing
import time

def cpu_intensive_task(n):
    result = 0
    for i in range(n):
        result += i
    return result

def multithreading_example():
    start_time = time.time()

    # Create threads
    thread1 = threading.Thread(target=cpu_intensive_task, args=(10**8,))
    thread2 = threading.Thread(target=cpu_intensive_task, args=(10**8,))

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
    process1 = multiprocessing.Process(target=cpu_intensive_task, args=(10**8,))
    process2 = multiprocessing.Process(target=cpu_intensive_task, args=(10**8,))

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