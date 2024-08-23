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


