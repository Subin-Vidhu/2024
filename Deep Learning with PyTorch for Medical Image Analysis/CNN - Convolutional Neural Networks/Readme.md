### CNN

- Understanding the MNIST dataset

    - The MNIST dataset is a collection of 70,000 images of handwritten digits from 0 to 9.

    - Each image is 28x28 pixels in size.

    - Each pixel in the image is represented by a value between 0 and 255.

    - The dataset is split into two parts:

        - 60,000 images for training.

        - 10,000 images for testing.

    - The MNIST dataset is a popular dataset for training and testing machine learning models.

    - It is often used as a benchmark dataset for evaluating the performance of different machine learning algorithms.

    - MNIST with ANN

        - First, we will train a simple artificial neural network (ANN) on the MNIST dataset.

        - For that, we have to flatten the 28x28 images into a single vector of size 784.

        - We will use a simple feedforward neural network with hidden layers.

        - We will use the softmax activation function in the output layer to get the probabilities of each class ie 0 to 9.

        - We will use the cross-entropy loss function to calculate the loss.

        - We will use the Adam optimizer to update the weights of the network.

        - We will train the network for 10 epochs.

        - We will evaluate the performance of the network on the test set.

            ![alt text](image.png)
            
        - Things to keep in mind:

            - Flattening out the images into a single vector of size 784 loses the spatial information present in the images ie it ends up removing some of the 2-D information present in the images, such as the relationship of a pixel to its neighbouring pixels.


