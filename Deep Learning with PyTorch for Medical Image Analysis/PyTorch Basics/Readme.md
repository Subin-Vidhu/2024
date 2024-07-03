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
            
            # torch.tensor vs torch.Tensor - torch.tensor always retains the datatype of the input data, while torch.Tensor(torch.FloatTensor) converts the datatype to the float32 tensor datatype.

            torch.empty(2, 2) # tensor([[1.4013e-45, 0.0000e+00],
                            #         [0.0000e+00, 0.0000e+00]])
            torch.zeros(2, 2) # tensor([[0., 0.],
                            #         [0., 0.]])
            torch.ones(2, 2) # tensor([[1., 1.],
                            #         [1., 1.]])
            torch.rand(2, 2) # tensor([[0.7645, 0.8303],
                            #         [0.2069, 0.6311]])
            torch.eye(2) # tensor([[1., 0.],

            #         [0., 1.]])
            torch.arange(0, 10, 2) # tensor([0, 2, 4, 6, 8])
            torch.linspace(0, 10, 5) # tensor([ 0.0000,  2.5000,  5.0000,  7.5000, 10.0000])
            torch.logspace(0, 10, 5) # tensor([1.0000e+00, 1.0000e+03, 1.0000e+06, 1.0000e+09, 1.0000e+10]) 

            # To convert into a particular datatype
            x = torch.tensor([1, 2, 3], dtype=torch.float32)
            print(x) # tensor([1., 2., 3.])
            #or
            arr = [1, 2, 3]
            arr.type(torch.float32)
            print(arr) # tensor([1., 2., 3.])

            # random number generation
            torch.manual_seed(42) # to ensure reproducibility
            torch.rand(2, 2) # tensor([[0.8823, 0.9150],
                            #         [0.3829, 0.9593]])
            torch.randn(2, 2) # tensor([[ 0.3367, -0.1288],
                            #         [ 0.2345,  0.2303]])
            torch.randint(0, 10, (5, 5)) # tensor([[6, 9, 2, 6, 7],
                                    #         [4, 3, 1, 3, 1],
                                    #         [3, 7, 3, 6, 7],
                                    #         [7, 2, 5, 4, 1],
                                    #         [4, 6, 6, 6, 6]])
            

            x = torch.zeros(2, 5)
            print(x) # tensor([[0., 0., 0., 0., 0.],
                    #         [0., 0., 0., 0., 0.]])
            print(x.shape()) # torch.Size([2, 5])
            torch.rand_like(x) # tensor([[0.8823, 0.9150, 0.3829, 0.9593, 0.3904],
                            #         [0.6009, 0.2566, 0.7936, 0.9408, 0.1332]])
            torch.zeros_like(x) # tensor([[0., 0., 0., 0., 0.],
                            #         [0., 0., 0., 0., 0.]])
            torch.ones_like(x) # tensor([[1., 1., 1., 1., 1.],
                            #         [1., 1., 1., 1., 1.]])

            torch.randn_like(x) # tensor([[ 0.3367, -0.1288,  0.2345,  0.2303, -0.6814],
                            #         [ 0.6472,  0.0726,  0.1991,  0.8657, -0.2673]])
            torch.randint_like(x, 0, 10) # tensor([[6, 9, 2, 6, 7],
                                    #         [4, 3, 1, 3, 1]])
                                    
            ```

- Tensor Operations

    - Element-wise operations
        - Element-wise operations are the operations between two tensors that operate on corresponding elements.

    - Broadcasting
        - Broadcasting is a powerful mechanism that allows PyTorch to work with arrays of different shapes when performing arithmetic operations.

    - Code:

        ```python
        import torch
        import numpy as np
        x = torch.arange(6).reshape(3, 2)
        x # tensor([[0, 1],
            #         [2, 3],
            #         [4, 5]])

        x[1, 1] # tensor(3)
        type(x[1, 1]) # torch.Tensor
        x[:,1]  # tensor([1, 3, 5])
        x[:,1:] # tensor([[1],
                #         [3],
                #         [5]])
        x[1:3, 0:2] # tensor([[2, 3],
                    #         [4, 5]])
        x[1:3, 0:2] = 0
        x # tensor([[0, 1],
            #         [0, 0],
            #         [0, 0]])
        
        #view() is used to reshape the tensor
        x = torch.arange(10)
        x # tensor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        x.view(2, 5) # tensor([[0, 1, 2, 3, 4],
                    #         [5, 6, 7, 8, 9]])
        x.view(5, 2) # tensor([[0, 1],
                    #         [2, 3],
                    #         [4, 5],
                    #         [6, 7],
                    #         [8, 9]])
        # view vs reshape - view() is a memory-efficient way to create a new tensor with the same data as the original tensor. If you modify the view, the original tensor will also be modified. If you want a new copy of the tensor, you should use the clone() method.

        # view reflects the original tensor