# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 08:54:29 2024

@author: Aus
"""

from sklearn.preprocessing import LabelEncoder

data = ['Red', 'Green', 'Blue', 'Red', 'Blue']
label_encoder = LabelEncoder()
encoded_data = label_encoder.fit_transform(data)

print(encoded_data)
# Output: [2 1 0 2 0]
