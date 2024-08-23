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

# Converting struct_time to Seconds (mktime)
seconds = time.mktime(parsed_time)
print(f"Seconds since epoch: {seconds}")

# Converting struct_time to String (asctime)
time_string = time.asctime(current_time_local)
print(f"Time as string: {time_string}")

# Using struct_time
print(f"Year: {current_time_local.tm_year}")
print(f"Month: {current_time_local.tm_mon}")
print(f"Day: {current_time_local.tm_mday}")
print(f"Hour: {current_time_local.tm_hour}")
print(f"Minute: {current_time_local.tm_min}")
print(f"Second: {current_time_local.tm_sec}")


# # sleep and performance measurement
import time

# Introducing Delays with sleep()
print("Start")
time.sleep(2)  # Pause for 2 seconds
print("End")

# Measuring Execution Time using time()
start_time = time.time()
for i in range(1000000):
    pass
end_time = time.time()
execution_time = end_time - start_time
print(f"Wall-clock time: {execution_time} seconds")

# Measuring Execution Time using perf_counter()
start_time = time.perf_counter()
for i in range(1000000):
    pass
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Performance counter time: {execution_time} seconds")

# Measuring CPU Time using process_time()
start_time = time.process_time()
for i in range(1000000):
    pass
end_time = time.process_time()
execution_time = end_time - start_time
print(f"CPU time (process): {execution_time} seconds")

# Measuring CPU Time using thread_time()
start_time = time.thread_time()
for i in range(1000000):
    pass
end_time = time.thread_time()
execution_time = end_time - start_time
print(f"CPU time (thread): {execution_time} seconds")