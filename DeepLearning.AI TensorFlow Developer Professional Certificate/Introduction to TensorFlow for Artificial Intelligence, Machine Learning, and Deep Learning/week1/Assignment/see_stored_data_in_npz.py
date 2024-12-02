# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:17:06 2024

@author: Subin-PC
"""

import numpy as np

a = np.load(r"D:\2024\DeepLearning.AI TensorFlow Developer Professional Certificate\Introduction to TensorFlow for Artificial Intelligence, Machine Learning, and Deep Learning\week1\Assignment\data\saved_arrays.npz")

print(a.files)  # Output: ['features', 'targets']

features = a['features']
print(features)  # Output: array([...])

targets = a['targets']
print(targets)  # Output: array([...])

# Alternatively, you can use the items() method to iterate over the key-value pairs in the npz file:
for key, value in a.items():
    print(f"{key}: {value}")
    
# features: [1. 2. 3. 4. 5. 6.]
# targets: [1.  1.5 2.  2.5 3.  3.5]