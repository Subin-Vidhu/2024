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

def allocate_gpu_memory():
    try:
        # Manually allocate memory until resource is exhausted
        # You can modify the size or create a larger model
        for _ in range(1000):  # Adjust the loop to control memory consumption
            tensor = tf.random.normal([1024, 1024, 1024])
            result = tf.math.add(tensor, tensor)
            print(f"Allocated tensor of shape {tensor.shape}")
    
    except ResourceExhaustedError as e:
        # Handle the GPU memory error
        print("Resource exhausted! Failed to allocate GPU memory.")
        print(str(e))
        
        # Manually clear the GPU memory and reset the session
        tf.keras.backend.clear_session()  # Clear session
        print("Cleared the GPU memory.")
    
    finally:
        # Optionally perform any final cleanup here
        pass

# Configure TensorFlow to use only as much GPU memory as needed (optional)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)  # Set memory growth
            print(f"Set memory growth for {gpu.name}")
    except RuntimeError as e:
        print(e)

# Call the function
allocate_gpu_memory()
from numba import cuda

cuda.close()
