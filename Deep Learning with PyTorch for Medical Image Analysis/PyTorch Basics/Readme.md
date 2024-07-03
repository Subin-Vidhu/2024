### Pytorch Basics

- What is PyTorch?
    - PyTorch is a Python-based scientific computing package serving two broad purposes:
        - A replacement for NumPy to use the power of GPUs
        - A deep learning research platform that provides maximum flexibility and speed
    - PyTorch is an open-source machine learning library for Python, based on Torch, used for applications such as natural language processing. It is primarily developed by Facebook's AI Research lab (FAIR), and Uber's Pyro software for probabilistic programming is built on it.
    - PyTorch provides two high-level features:
        - Tensor computation (like NumPy) with strong GPU acceleration
        - Deep neural networks built on a tape-based autograd system
    
- PyTorch Tensors

    - Often thought of as a generalization of a matrix, a tensor is an array with an arbitrary number of axes. A matrix is a tensor with two axes, and a scalar is a tensor with zero axes.

        ![alt text](image.png)

    - Tensors are similar to NumPy's ndarrays, with the addition being that Tensors can also be used on a GPU to accelerate computing.
    - Tensors are multi-dimensional arrays with support for automatic differentiation.
    - PyTorch has a rich library for operations on Tensors.
    - Tensors are the basic building blocks of PyTorch.
    
- Why do we use tensors?

    - Easiest to arrange data in the form of tensors.

- Tensor Basics

    - A tensor is a generalization of vectors and matrices and is easily understood as a multidimensional array.
    - A PyTorch Tensor is conceptually identical to a NumPy array.
    - A tensor is an n-dimensional array.
    - A tensor can be thought of as a generalized matrix.
    - A tensor is a fundamental data structure for deep learning.
    - Tensors are used to encode the signal, image, and other data types.
    
        - Python code:
            ```python
            import torch
            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            print(arr)
            type(arr) # numpy.ndarray
            x = torch.from_numpy(arr)
            print(x) # tensor([1, 2, 3, 4, 5], dtype=torch.int32)
            type(x) # torch.Tensor
            x = torch.as_tensor(arr)
            print(x) # tensor([1, 2, 3, 4, 5], dtype=torch.int32)
            type(x) # torch.Tensor
            x.dtype # torch.int32

            #2D
            arr_2d = np.arange(0.0, 12.0).reshape(4, 3)
            print(arr_2d) # [[ 0.  1.  2.]
                          #  [ 3.  4.  5.]
                          #  [ 6.  7.  8.]
                          #  [ 9. 10. 11.]]
            x_2d = torch.from_numpy(arr_2d)
            print(x_2d) # tensor([[ 0.,  1.,  2.],
                        #         [ 3.,  4.,  5.],
                        #         [ 6.,  7.,  8.],
                        #         [ 9., 10., 11.]], dtype=torch.float64)

            arr[0] = 99
            print(x) # tensor([99,  2,  3,  4,  5], dtype=torch.int32)
            # The tensor and the NumPy array share the same memory location.To only share a copy of the data, use torch.tensor() instead of torch.from_numpy().
            x = torch.tensor(arr)
            arr[0] = 100
            print(arr) # [100   2   3   4   5]
            print(x) # tensor([99,  2,  3,  4,  5], dtype=torch.int32)
            #torch.Tensor converts the datatype
            ```