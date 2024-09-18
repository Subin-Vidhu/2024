# import GPUtil
# import psutil

# def get_gpu_info():
#     # Get list of all GPUs
#     gpus = GPUtil.getGPUs()
    
#     if not gpus:
#         print("No GPU found on this system.")
#         return
    
#     for gpu in gpus:
#         print(f"GPU Name: {gpu.name}")
#         print(f"  Total GPU Memory: {gpu.memoryTotal} MB")
#         print(f"  Free GPU Memory: {gpu.memoryFree} MB")
#         print(f"  Used GPU Memory: {gpu.memoryUsed} MB")
#         print(f"  GPU Load: {gpu.load * 100}%")
#         print(f"  GPU Temperature: {gpu.temperature} °C\n")

# if __name__ == "__main__":
#     get_gpu_info()

import tensorflow as tf
from tensorflow.python.framework.errors_impl import ResourceExhaustedError
from numba import cuda

def print_gpu_memory_info():
    # Retrieve memory info for each GPU
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            device_name = gpu.name.replace('/physical_device:', '')  # Extract "GPU:0"
            try:
                # Retrieve and print memory info
                gpu_details = tf.config.experimental.get_memory_info(device_name)
                total_memory = gpu_details['current']  # Current allocated memory
                available_memory = gpu_details['peak']  # Peak allocated memory
                print(f"GPU: {device_name}")
                print(f"  Total Memory: {total_memory / (1024 ** 2)} MB")  # Convert to MB
                print(f"  Available Memory: {available_memory / (1024 ** 2)} MB")
            except Exception as e:
                print(f"Failed to get memory info for {device_name}: {str(e)}")
    else:
        print("No GPU found.")

def allocate_gpu_memory():
    try:
        print("Allocating memory...")
        # Print initial memory info
        print_gpu_memory_info()
        
        # Manually allocate memory until resource is exhausted
        for _ in range(1000):  # Adjust the loop to control memory consumption
            tensor = tf.random.normal([1024, 1024, 1024])
            result = tf.math.add(tensor, tensor)
            print(f"Allocated tensor of shape {tensor.shape}")
            print_gpu_memory_info()  # Check memory after allocation
    
    except ResourceExhaustedError as e:
        # Handle the GPU memory error
        print("Resource exhausted! Failed to allocate GPU memory.")
        print(str(e))
        
        # Manually clear the GPU memory and reset the session
        tf.keras.backend.clear_session()  # Clear session
        print("Cleared the GPU memory.")
        print_gpu_memory_info()  # Check memory after clearing
    
    finally:
        print("Memory allocation completed.")
        print_gpu_memory_info()  # Final check

# Configure TensorFlow to use only as much GPU memory as needed (optional)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)  # Set memory growth
            print(f"Set memory growth for {gpu.name}")
    except RuntimeError as e:
        print(e)

# Call the function to allocate memory
allocate_gpu_memory()

# Release GPU resources using Numba (optional)
cuda.close()
