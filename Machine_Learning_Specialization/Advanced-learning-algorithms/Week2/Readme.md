## Images for Reference

- Train a neural network in Tensorflow

    ![alt text](image.png)

- Model Training Steps

    ![alt text](image-1.png)

    - Create a model
     
        ![alt text](image-2.png)

    - Loss function and Cost function

        ![alt text](image-3.png)

    - Gradient Descent

        ![alt text](image-4.png)

- Activation Functions

    - Sigmoid, ReLU, Linear and many more

        ![alt text](image-5.png)

    
    - Choosing the right activation function

        ![alt text](image-6.png)

        ![alt text](image-7.png)

        ![alt text](image-8.png)
    
    - Why do we need activation functions?

        - Without activation functions, the neural network is just a linear regression model.

        - Activation functions introduce non-linearity to the model. Non-linearity is important because most real-world data is non-linear.

        - Activation functions help the neural network to learn complex patterns in the data.

        - eg.

            ```python
            def sigmoid(x):
                return 1 / (1 + np.exp(-x))
            ```

- Multiclass classification

    - more than 2 possible outputs

        ![alt text](image-9.png)


- Softmax function

    - Multiclass classification

        ![alt text](image-10.png)

    - Cost function

        ![alt text](image-11.png)

    - Neurel Network with Softmax

        ![alt text](image-12.png)

    - Improved implementation

        ![alt text](image-13.png)

        ![alt text](image-15.png)

        ![alt text](image-14.png)

        ![alt text](image-16.png)

- Multi label classification

    - Train one neural network to predict multiple labels

        ![alt text](image-17.png)

- Gradient Descent

    - Gradient Descent is an optimization algorithm used to minimize some function by iteratively moving in the direction of steepest descent as defined by the negative of the gradient.

        ![alt text](image-18.png)

    - Adam

        ![alt text](image-19.png)

- Additional Layer Types

    - Convolutional Neural Networks

        - Convolutional Neural Networks are a type of deep learning algorithm that can take in an input image, assign importance to various aspects/objects in the image and be able to differentiate one from the other.

            ![alt text](image-20.png)

