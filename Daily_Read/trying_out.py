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