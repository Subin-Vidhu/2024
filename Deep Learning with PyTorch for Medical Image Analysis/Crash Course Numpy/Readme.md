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
    ```