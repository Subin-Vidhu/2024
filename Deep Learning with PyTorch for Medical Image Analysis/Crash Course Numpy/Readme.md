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
    type(arr) # output: numpy.ndarray

    my_matrix = [[1,2,3],[4,5,6],[7,8,9]]
    type(my_matrix) # output: list
    matrix = np.array(my_matrix)
    print(matrix) # output: array([[1, 2, 3],#[4, 5, 6],#[7, 8, 9]])
    type(matrix) # output: numpy.ndarray
    print(matrix.shape) # output: (3, 3)

    # arange
    np.arange(0,10) # output: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    np.arange(0,11,2) # output: array([ 0,  2,  4,  6,  8, 10])

    # zeros and ones
    np.zeros(3) # output: array([0., 0., 0.])
    np.zeros((5,5)) # output: array([[
    # 0., 0., 0., 0., 0.],
    # [0., 0., 0., 0., 0.],
    # [0., 0., 0., 0., 0.],
    # [0., 0., 0., 0., 0.],
    # [0., 0., 0., 0., 0.]])
    np.ones(3) # output: array([1., 1., 1.])
    np.ones((3,3)) # output: array([[1., 1., 1.],
    # [1., 1., 1.],
    # [1., 1., 1.]])
    # By default, the data type of the created array is float64. We can specify the data type by using the dtype parameter.

    # Broadcasting with ones
    np.ones(3,3) + 4 # output: array([[5., 5., 5.],
    # [5., 5., 5.],
    # [5., 5., 5.]])
    np.ones(3,3) * 4 # output: array([[4., 4., 4.],
    # [4., 4., 4.],
    # [4., 4., 4.]])

    # linspace
    np.linspace(0,10,3) # output: array([ 0.,  5., 10.])
    np.linspace(0,10,5) # output: array([ 0.,  2.5,  5.,  7.5, 10.])

    # eye
    np.eye(4) # output: array([[1., 0., 0., 0.],
    # [0., 1., 0., 0.],
    # [0., 0., 1., 0.],
    # [0., 0., 0., 1.]])
    np.eye(3) # output: array([[1., 0., 0.],
    # [0., 1., 0.],
    # [0., 0., 1.]])

    # Random
    np.random.rand(2) # output: array([0.4359949 , 0.02592623])
    # random numbers from a uniform distribution over [0, 1), mean 0 and variance 0
    np.random.randn(2) # output: array([ 0.86617615, -0.67888615])
    # random numbers from a normal distribution with mean 0 and variance 1
    np.random.randint(1,100,10) # output: array([ 9, 77, 40,  4, 63, 40, 60, 92, 64,  5])
    # random integers from low (inclusive) to high (exclusive)
    np.random.seed(42) # as long as the seed remains the same, the random numbers will be the same [but not in the next cell, ie both the seed and the random number generation should be in the same cell]

    # Reshape
    arr = np.arange(25)
    print(arr) # output: array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    arr.reshape(5,5) # output: array([[ 0,  1,  2,  3,  4],
    # [ 5,  6,  7,  8,  9],
    # [10, 11, 12, 13, 14],
    # [15, 16, 17, 18, 19],
    # [20, 21, 22, 23, 24]])

    # max, min, argmax, argmin
    arr = np.random.randint(0,50,10)
    print(arr) # output: array([38, 18, 22, 10, 10, 23, 35, 39, 23,  2])
    arr.max() # output: 39
    arr.argmax() # output: 7
    arr.min() # output: 2
    arr.argmin() # output: 9

    # shape
    arr = np.arange(10)
    arr.shape # output: (10,)
    arr = arr.reshape(2,5)
    print(arr) # output: array([[38, 18, 22, 10, 10],
    # [23, 35, 39, 23,  2]])
    arr.shape # output: (2, 5)

    # dtype
    arr.dtype # output: dtype('int64')
    arr = np.array([1.0,2.0,3.0])
    arr.dtype # output: dtype('float64')

    # Indexing and Selection
    arr = np.arange(0,11)
    print(arr) # output: array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
    arr[8] # output: 8
    arr[1:5] # output: array([1, 2, 3, 4])
    arr[:6] # output: array([0, 1, 2, 3, 4, 5])
    arr[5:] # output: array([ 5,  6,  7,  8,  9, 10])
    arr[0:5] = 100
    print(arr) # output: array([100, 100, 100, 100, 100, 5, 6, 7, 8, 9, 10])
    arr = np.arange(0,11)
    slice_of_arr = arr[0:6]
    print(slice_of_arr) # output: array([0, 1, 2, 3, 4, 5])
    slice_of_arr[:] = 99
    print(slice_of_arr) # output: array([99, 99, 99, 99, 99, 99])
    print(arr) # output: array([99, 99, 99, 99, 99, 99,  6,  7,  8,  9, 10])

    # Copy - slicing creates a view of the original array, not a copy, so changes to the slice will affect the original array. If you dont want the original array to be affected, you should make a copy of the array

    arr_copy = arr.copy()
    arr_copy[:] = 100
    print(arr) # output: array([99, 99, 99, 99, 99, 99,  6,  7,  8,  9, 10])
    print(arr_copy) # output: array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100])

    # Indexing a 2D array
    arr_2d = np.array([[5,10,15],[20,25,30],[35,40,45]])
    print(arr_2d) # output: array([[ 5, 10, 15],
    # [20, 25, 30],
    # [35, 40, 45]])
    arr_2d[0] # output: array([ 5, 10, 15])
    arr_2d[1][0] # output: 20
    arr_2d[:2,1:] # output: array([[10, 15],
    # [25, 30]])
    arr_2d[2] # output: array([35, 40, 45])
    arr_2d[2,:] # output: array([35, 40, 45])
    arr_2d.shape # output: (3, 3)

    # Conditional Selection
    arr = np.arange(1,11)
    print(arr) # output: array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
    bool_arr = arr > 5
    print(bool_arr) # output: array([False, False, False, False, False,  True,  True,  True,  True,  True])
    arr[bool_arr] # output: array([ 6,  7,  8,  9, 10])
    arr[arr>5] # output: array([ 6,  7,  8,  9, 10])
    arr[arr<3] # output: array([1, 2])
    arr_2d = np.arange(50).reshape(5,10)
    print(arr_2d) # output: array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
    # [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    # [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    # [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    # [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]])
    arr_2d[arr_2d>25] # output: array([26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49])

    # Operations
    arr = np.arange(0,10)
    print(arr) # output: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    arr + arr # output: array([ 0,  2,  4,  6,  8, 10, 12, 14, 16, 18])
    arr * arr # output: array([ 0,  1,  4,  9, 16, 25, 36, 49, 64, 81])
    arr - arr # output: array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    arr / arr # output: array([nan,
    # 1., 1., 1., 1., 1., 1., 1., 1., 1.])
    1/arr # output: array([       inf, 1.        , 0.5       , 0.33333333, 0.25      ,
    # 0.2       , 0.16666667, 0.14285714, 0.125     , 0.11111111])
    arr ** 2 # output: array([ 0,  1,  4,  9, 16, 25, 36, 49, 64, 81])
    np.sqrt(arr) # output: array([0.        , 1.        , 1.41421356, 1.73205081, 2.        ,
    # 2.23606798, 2.44948974, 2.64575131, 2.82842712, 3.        ])
    np.exp(arr) # output: array([1.00000000e+00, 2.71828183e+00, 7.38905610e+00, 2.00855369e+01,
    # 5.45981500e+01, 1.48413159e+02, 4.03428793e+02, 1.09663316e+03,
    # 2.98095799e+03, 8.10308393e+03])
    np.max(arr) # output: 9
    np.sum(arr) # output: 45
    
    ```