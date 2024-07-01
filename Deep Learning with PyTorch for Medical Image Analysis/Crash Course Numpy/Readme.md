# Crash Course Numpy

- What is Numpy?

    - Python library for creating N-dimensional arrays
    - ability to quickly broadcast functions
    - built in linear algebra, statistical distributions, trigonometric and random number capabilities

- Why use Numpy?

    - While numpy structures look similar to standard python lists, they are much more efficient
    - Numpy arrays are stored at one continuous place in memory unlike lists, so processes can be performed on them much faster
    - Numpy is optimized for numerical operations and is faster than standard python lists

- Numpy Arrays

    - Numpy arrays are the main way we will use numpy
    - Numpy arrays essentially come in two flavors: vectors and matrices
    - Vectors are strictly 1-d arrays and matrices are 2-d (but you should note a matrix can still have only one row or one column)

    - eg:
    ```python
    import numpy as np

    my_list = [1,2,3]
    type(my_list) # output: list
    arr = np.array(my_list)
    print(arr) # output: array([1, 2, 3]) 
    ```