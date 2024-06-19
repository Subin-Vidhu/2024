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