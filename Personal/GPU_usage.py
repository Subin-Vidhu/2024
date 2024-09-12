# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 13:23:47 2024

@author: Subin-PC
"""

import GPUtil
import psutil

def get_gpu_info():
    # Get list of all GPUs
    gpus = GPUtil.getGPUs()
    
    if not gpus:
        print("No GPU found on this system.")
        return
    
    for gpu in gpus:
        print(f"GPU Name: {gpu.name}")
        print(f"  Total GPU Memory: {gpu.memoryTotal} MB")
        print(f"  Free GPU Memory: {gpu.memoryFree} MB")
        print(f"  Used GPU Memory: {gpu.memoryUsed} MB")
        print(f"  GPU Load: {gpu.load * 100}%")
        print(f"  GPU Temperature: {gpu.temperature} °C\n")

if __name__ == "__main__":
    get_gpu_info()
