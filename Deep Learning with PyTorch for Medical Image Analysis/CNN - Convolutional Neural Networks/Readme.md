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

        - Code:

            -   ```python
                import torch
                import torch.nn as nn
                import torch.nn.functional as F
                from torch.utils.data import DataLoader
                from torchvision import datasets, transforms
                import matplotlib.pyplot as plt
                import numpy as np
                from sklearn.metrics import confusion_matrix
                %matplotlib inline

                # Load the MNIST dataset
                transform = transforms.ToTensor()
                train_data = datasets.MNIST(root='data', train=True, download=True, transform=transform)
                test_data = datasets.MNIST(root='data', train=False, download=True, transform=transform)
                print(train_data) #Dataset MNIST
                                    #Number of datapoints: 60000
                                    #Split: train
                                    #Root Location: data
                                    #Transforms (if any): ToTensor()
                                    #Target Transforms (if any): None
                print(test_data) #Dataset MNIST
                                    #Number of datapoints: 10000
                                    #Split: test
                                    #Root Location: data
                                    #Transforms (if any): ToTensor()
                                    #Target Transforms (if any): None

                type(train_data) #torchvision.datasets.mnist.MNIST
                train_data[0] #Returns a tuple of image and label
                image, label = train_data[0]
                image.shape #torch.Size([1, 28, 28])
                label #5
                plt.imshow(image.reshape(28, 28), cmap='gray') #cmap = 'gray' is used to display the image in grayscale, use 'viridis' for color, use 'gist_yarg' for opposite grayscale

                torch.manual_seed(101) #arbitrary seed for reproducibility
                train_loader = DataLoader(train_data, batch_size=100, shuffle=True)
                test_loader = DataLoader(test_data, batch_size=500, shuffle=False)

                from torchvision.utils import make_grid
                np.set_printoptions(formatter=dict(int=lambda x: f'{x:4}')) # to widen the printed array

                # Display the first batch of images
                for images, labels in train_loader:
                    break

                images.shape #torch.Size([100, 1, 28, 28]) - 100 images, 1 channel(colour channel, 1 since it is a gray scale image), 28x28 pixels(height x width)
                labels.shape #torch.Size([100])

                # Print the first 12 labels
                print('Labels: ', labels[:12].numpy()) #Labels:  [   5    0    4    1    9    2    1    3    1    4    3    5]

                # Print the first 12 images
                im = make_grid(images[:12], nrow=12) #nrow is the number of images in each row
                plt.figure(figsize=(10, 4))
                # We need to transpose the images from CWH to WHC
                plt.imshow(np.transpose(im.numpy(), (1, 2, 0))) #transpose is used to change the order of the dimensions
                ```
                ![alt text](image-1.png)
                ```python
                # Create the model
                class MultilayerPerceptron(nn.Module):
                    def __init__(self, in_sz=784, out_sz=10, layers=[120, 84]):
                        super().__init__() #super() is used to call the __init__() of the parent class so that we can access the attributes of the parent class
                        self.fc1 = nn.Linear(in_sz, layers[0])
                        self.fc2 = nn.Linear(layers[0], layers[1])
                        self.fc3 = nn.Linear(layers[1], out_sz)

                    def forward(self, X):
                        X = F.relu(self.fc1(X))
                        X = F.relu(self.fc2(X))
                        X = self.fc3(X)
                        return F.log_softmax(X, dim=1) #dim=1 is used to specify the dimension along which the softmax function is to be applied

                torch.manual_seed(101)
                model = MultilayerPerceptron()
                model
                # MultilayerPerceptron(
                #   (fc1): Linear(in_features=784, out_features=120, bias=True)
                #   (fc2): Linear(in_features=120, out_features=84, bias=True)
                #   (fc3): Linear(in_features=84, out_features=10, bias=True)
                # )

                for param in model.parameters():
                    print(param.numel()) 
                    # 94080 - 784*120 weights
                    # 120 - 120 bias
                    # 10080 - 120*84 weights
                    # 84 - 84 bias
                    # 840 - 84*10 weights
                    # 10 - 10 bias
                    # Total = 105,214 parameters