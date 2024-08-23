import time

# Getting the Current Time
current_time = time.time()
print(f"Current time: {current_time}")

# Converting Time to a String
time_string = time.ctime(current_time)
print(f"Current time as string: {time_string}")

# Formatting Time with strftime()
current_time_local = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time_local)
print(f"Formatted time: {formatted_time}")

# Parsing Time with strptime()
time_string = "2023-05-17 14:30:00"
parsed_time = time.strptime(time_string, "%Y-%m-%d %H:%M:%S")
print(f"Parsed time: {parsed_time}")


# sleep and performance measurement
import time

# Introducing Delays with sleep()
print("Start")
time.sleep(2)  # Pause for 2 seconds
print("End")

# Measuring Execution Time
start_time = time.time()

# Your code here
for i in range(1000000):
    pass

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


# Time Module in Python
# The time module in Python provides various time-related functions. It allows you to handle time in different formats, perform conversions between different time formats, and measure the execution time of your code.

# Table of Contents
# Importing the Time Module
# Time Functions
# Advanced Options
# Best Practices
# Example Code
# Importing the Time Module
# To use the time module, you need to import it at the beginning of your Python script:

# import time
# Time Functions
# 1. time.time()
# This function returns the current system time in seconds since the epoch (January 1, 1970).

# 2. time.localtime()
# This function returns the current local time as a struct_time object.

# 3. time.gmtime()
# This function returns the current UTC time as a struct_time object.

# 4. time.sleep()
# This function suspends the execution of the current thread for the given number of seconds.

# 5. time.strftime()
# This function converts a struct_time object to a string in the specified format.

# 6. time.strptime()
# This function converts a string to a struct_time object in the specified format.

# 7. time.mktime()
# This function converts a struct_time object to seconds since the epoch.

# 8. time.asctime()
# This function converts a struct_time object to a string in the format "Day Mmm DD HH:MM:SS YYYY".

# 9. time.ctime()
# This function converts seconds since the epoch to a string in the format "Day Mmm DD HH:MM:SS YYYY".

# 10. time.perf_counter()
# This function returns the value (in fractional seconds) of a performance counter, which is a clock with the highest available resolution to measure a short duration.

# 11. time.process_time()
# This function returns the sum of the system and user CPU time of the current process.

# 12. time.thread_time()
# This function returns the sum of the system and user CPU time of the current thread.

# Advanced Options
# 1. time.struct_time
# This is a class that represents a time as a tuple of nine integers.

# 2. time.tzset()
# This function sets the timezone based on the environment variable TZ.

# 3. time.altzone
# This is a constant that represents the offset of the alternate timezone in seconds.

# 4. time.daylight
# This is a constant that represents whether the timezone uses daylight saving time.

# 5. time.timezone
# This is a constant that represents the offset of the local timezone in seconds.

# 6. time.tzname
# This is a constant that represents the name of the local timezone.

# Best Practices
# Use time.time() to get the current time in seconds since the epoch.
# Use time.localtime() to get the current local time as a struct_time object.
# Use time.strftime() to convert a struct_time object to a string in the specified format.
# Use time.strptime() to convert a string to a struct_time object in the specified format.
# Use time.sleep() to suspend the execution of the current thread for the given number of seconds.
# Use time.perf_counter() to measure the execution time of your code.
# Use time.process_time() to measure the CPU time of the current process.
# Use time.thread_time() to measure the CPU time of the current thread.
# Example Code
# Example 1: Get the current time in seconds since the epoch
# import time
# print(time.time())
# Example 2: Get the current local time as a struct_time object
# import time
# print(time.localtime())
# Example 3: Convert a struct_time object to a string in the specified format
# import time
# print(time.strftime("%Y-%m-%d %H:%M:%S"))
# Example 4: Measure the execution time of your code
# import time
# start_time = time.perf_counter()
# # Your code here
# end_time = time.perf_counter()
# print(f"Execution time: {end_time - start_time} seconds")
# Example 5: Measure the CPU time of the current process
# import time
# start_time = time.process_time()
# # Your code here
# end_time = time.process_time()
# print(f"CPU time: {end_time - start_time} seconds")
# Example 6: Measure the CPU time of the current thread
# import time
# start_time = time.thread_time()
# # Your code here
# end_time = time.thread_time()
# print(f"CPU time: {end_time - start_time} seconds")