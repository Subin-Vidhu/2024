## References

- Deep Neural Network

    - neural network with more than one hidden layer.

        ![alt text](image.png)

    - Notation

        - L: number of layers in the network
        - n[l]: number of units in layer l
        - a[l]: activation in layer l
        - W[l]: weights for z[l]
        - b[l]: bias for z[l]
        - z[l]: linear function of the previous layer
        - g[l]: activation function for layer l
        - a[0] = x

            ![alt text](image-1.png)

    - Forward Propagation

        - Compute z[l] = W[l]a[l-1] + b[l]
        - Compute a[l] = g[l](z[l]) = g[l](W[l]a[l-1] + b[l])
        - Compute for l = 1 to L

            ![alt text](image-2.png)
