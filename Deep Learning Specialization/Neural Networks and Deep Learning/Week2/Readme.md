## References

- Logistic Regression

    -  algorithm for binary classification
    -  used for spam detection, image recognition, etc.
        eg. cat vs non-cat

        ![alt text](image.png)

- Notation

    -  m: number of training examples
    -  n: number of features
    -  x: input vector
    -  y: output vector
    -  (x, y): one training example
    -  (x(i), y(i)): ith training example
    -  X: matrix of input vectors
    -  Y: matrix of output vectors

        ![alt text](image-1.png)

- Logistic Regression

    - given x, want y-hat = P(y = 1 | x)
    - parameters: w, b
    - output: y-hat = sigmoid(w^T x + b)
    - sigmoid function: 1 / (1 + e^(-z))

        ![alt text](image-2.png)

- Logistic Regression Cost Function

    - loss (single example): L(y-hat, y) = -(y log(y-hat) + (1 - y) log(1 - y-hat))
    - cost (all examples): J(w, b) = (1 / m) * sum(L(y-hat, y))

        ![alt text](image-3.png)

- Gradient Descent

    - update parameters: w = w - alpha * dw, b = b - alpha * db
    - dw = (1 / m) * sum(dL/dw), db = (1 / m) * sum(dL/db)

        ![alt text](image-4.png)

        ![alt text](image-5.png)

- Intuition about derivatives

    - derivative: slope of a function
    - if slope > 0: increase parameter
    - if slope < 0: decrease parameter
    - if slope = 0: parameter is optimal

        ![alt text](image-6.png)

        ![alt text](image-7.png)

        ![alt text](image-8.png)

- Computation Graph

    - visualize computation
    - forward propagation: compute output
    - backward propagation: compute derivatives

        ![alt text](image-9.png)

        ![alt text](image-10.png)

- Logistic Regression Derivatives

    - dz = y-hat - y
    - dw = (1 / m) * x * dz^T
    - db = (1 / m) * sum(dz)

        ![alt text](image-12.png)

- Vectorization

    - avoid explicit loops
    - use matrix operations
    - faster, simpler code

        ![alt text](image-13.png)

        ![alt text](image-14.png)

        ![alt text](image-15.png)

- Broadcasting

    - extend smaller array
    - perform operation

       ![alt text](image-16.png) 

       ![alt text](image-17.png)

       ![alt text](image-18.png)

- Python/Numpy Vectors

    - always use vectors
    - avoid rank 1 arrays

        ![alt text](image-20.png)