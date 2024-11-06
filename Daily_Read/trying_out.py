# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 08:54:29 2024

@author: Aus
"""
####### 1. LE vs OHE #######

# Label Encoder
from sklearn.preprocessing import LabelEncoder

data = ['Red', 'Green', 'Blue', 'Red', 'Blue']
label_encoder = LabelEncoder()
encoded_data = label_encoder.fit_transform(data)

print(encoded_data)
# Output: [2 1 0 2 0]


# One Hot Encoding
from sklearn.preprocessing import OneHotEncoder
import numpy as np

data = np.array(['Red', 'Green', 'Blue', 'Red', 'Blue']).reshape(-1, 1) 
#.reshape(-1, 1):
# Reshapes the array into a 2-dimensional array (matrix) with one column and as many rows as needed.
# The -1 argument means "infer the number of rows from the length of the array," effectively turning the 1D array into a column vector.
#The resulting shape of the array will be (5, 1), where 5 is the number of rows, and 1 is the number of columns.
#  array([
#     ['Red'],
#     ['Green'],
#     ['Blue'],
#     ['Red'],
#     ['Blue']
# ])

one_hot_encoder = OneHotEncoder(sparse=False) 
# sparse=False:

#The sparse parameter specifies the type of the matrix to return.
#If sparse=True (the default), the encoder returns a sparse matrix. Sparse matrices are efficient for storing large, sparse datasets because they only store non-zero entries, saving memory.
#If sparse=False, the encoder returns a dense NumPy array. Dense matrices store all entries, including zeros.
# In this example, sparse=False is used, meaning the output will be a dense NumPy array

encoded_data = one_hot_encoder.fit_transform(data)

print(encoded_data)
# Output:
# [[0. 0. 1.]
#  [0. 1. 0.]
#  [1. 0. 0.]
#  [0. 0. 1.]
#  [1. 0. 0.]]


######## Flatten #######

a = np.array([[1, 2, 3],
            [4, 5, 6]])
    
a.flatten()
# Out[21]: array([1, 2, 3, 4, 5, 6])

################ .ravel() vs .flatten() ############

import numpy as np

# Create a 2D array
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Use .ravel() to flatten the array
flattened_arr_ravel = arr.ravel()

# Use .flatten() to flatten the array
flattened_arr_flatten = arr.flatten()

# Modify the returned arrays
flattened_arr_flatten[0] = 20
flattened_arr_ravel[0] = 10


print("Original array:")
print(arr)

print("\nReturned array from .ravel():")
print(flattened_arr_ravel)

print("\nReturned array from .flatten():")
print(flattened_arr_flatten)

# Original array:
# [[10  2  3]
#  [ 4  5  6]]

# Returned array from .ravel():
# [10  2  3  4  5  6]

# Returned array from .flatten():
# [20  2  3  4  5  6]
############## **kwargs ###############

def hello(**kwargs):
    #print("Hello " + kwargs['first'] + " " + kwargs['last']) # Hello Bro Code
    print("Hello",end=" ")
    for key,value in kwargs.items():
        print(value,end=" ")


hello(title="Mr.",first="Bro",middle="Dude",last="Code")


####################### f-strings ###############
name = "Bro"

print(f"My name is {name}")
print(f"My name is {name:10}")  # amount of padding
print(f"My name is {name:<10}")  # < = left align
print(f"My name is {name:>10}")  # > = right align
print(f"My name is {name:^10}")  # ^ = center align

# My name is Bro
# My name is Bro       
# My name is Bro       
# My name is        Bro
# My name is    Bro


# Using f-string with format specifiers
number = 1000
print(f"The number pi is {number:.3f}")
print(f"The number is {number:,}")
print(f"The number is {number:b}")
print(f"The number is {number:o}")
print(f"The number is {number:X}")
print(f"The number is {number:E}")
# The number pi is 1000.000
# The number is 1,000
# The number is 1111101000
# The number is 1750
# The number is 3E8
# The number is 1.000000E+03


################# Threading #############

import threading
import time


def eat_breakfast():
    time.sleep(3)
    print("You eat breakfast")


def drink_coffee():
    time.sleep(4)
    print("You drank coffee")


def study():
    time.sleep(5)
    print("You finish studying")


x = threading.Thread(target=eat_breakfast, args=())
x.start()

y = threading.Thread(target=drink_coffee, args=())
y.start()

z = threading.Thread(target=study, args=())
z.start()

x.join()
y.join()
z.join()

print(threading.active_count())
print(threading.enumerate())
print(time.perf_counter())

######
import threading
import time

def eat_breakfast():
    time.sleep(3)
    print("You eat breakfast")

def drink_coffee():
    time.sleep(4)
    print("You drank coffee")

def study():
    time.sleep(5)
    print("You finish studying")

x = threading.Thread(target=eat_breakfast, args=())
y = threading.Thread(target=drink_coffee, args=())
z = threading.Thread(target=study, args=())

x.start()
y.start()
z.start()

# Without join(), the main thread will terminate immediately
print("Main thread terminated")

# With join(), the main thread will wait for all threads to finish
# x.join()
# y.join()
# z.join()

########################## RGB to grayscale #########################
# Import the modules from skimage
from skimage import data, color

# Load the rocket image
rocket = data.rocket()

# Convert the image to grayscale
gray_scaled_rocket = color.rgb2gray(rocket)

# Show the original image
show_image(rocket, 'Original RGB image')

# Show the grayscale image
show_image(gray_scaled_rocket, 'Grayscale image')

import matplotlib.pyplot as plt
def show_image(image, title='Image', cmap_type='gray'):
    plt.imshow(image, cmap=cmap_type)
    plt.title(title)
    plt.axis('off')
    plt.show()
    
################### Creating a Zero Array with np.zeros #################
import numpy as np

# Create a sample image array
image = np.random.rand(512, 512, 3)

# Get the shape of the image
print(image.shape)  # Output: (512, 512, 3)
test_image = image[:,:,1]
print(test_image.shape) # Output: (512, 512)
# Create a zero array with the same shape as the image, but with one less dimension
zero_array = np.zeros(image.shape[:-1])

# Print the shape of the zero array
print(zero_array.shape)  # Output: (512, 512)


# Bag of Words
from collections import Counter
import re

def create_bow(text):
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    
    # Split the text into words
    words = text.split()
    
    # Create a BoW representation using Counter
    bow = Counter(words)
    
    return bow

# Example usage
text = "The quick brown fox jumps over the lazy dog."
bow = create_bow(text)

print(bow)