### Atrium Segmentation

- **Task**: Automatically segment the left atrium in cardiac MR images.

- Medical Background

    - Atrium Segmentation classifies each voxel in the MRI into either "Not Left Atrium" or "Left Atrium".

    - Enables exact volume measurements of the left atrium.

    - Changes in atrial volume are associated with cardiac disorders, such as atrial fibrillation or mitral valve stenosis(Narrowing of the mitral valve orifice, blocking blood flow).

    - Manual segmentation is time-consuming and tedious - Automation is needed.

- Data

    - Medical Segmentation Decathlon dataset [Link](http://medicaldecathlon.com/dataaws/)

    - 20 cardiac MR images with corresponding Ground Truth masks.

        - 4542 2D MRI and label slices.

- Preprocessing

    - Two dimensional setting, Extract slices.

    - Original image shape (352 * 352)

        - Crop away non-cardiac regions and background.

            - 32 pixel from all borders

            - **Also applied to segmentation mask**

    - Z-Normalization per subject

        - Compute mean and standard deviation for each subject separately.

    - Standardize the normalized subject into the interval [0, 1]

        - X_std = (X_n - min(X_n)) / (max(X_n) - min(X_n))

    - Use 16 patients as training data and the remaining 4 as validation data.

- Dataset

    - Task

        - Create a list of all 2D slices and their corresponding masks.
        - Extract and load slice and mask from the list.
        - Data Augmentation: Augment slice and mask identically
        - Return augmented slice and mask.

    - Data Augmentation

        - Scaling (0.85, 1.15)
        - Rotation (-45, 45)
        - Elastic Transformation - augment the image by moving the pixels locally around using a displacement field.

- Model

    - U-Net(Miccai, 2015)

        - Encoder-Decoder architecture with skip connections.

            - Encoder: Convolutional layers with max pooling.

                - reduces the feature maps by using convolutions + max pooling.

        - Decoder: Convolutional layers with upsampling.
            
                - reconstructs segmentation masks based on the original image and features by using Upsampling + Convolutional layers.

        - Skip connections: Concatenate encoder output with decoder input.

            - allow information flow from encoder to decoder, this directly allows to solve the problem of vanishing gradients.(Vanishing gradients occur when the gradients become very small and the network stops learning.)
            

                <!-- ![alt text](image.png) -->
                <img src="image.png" width="300" height="300">

- Training

    - Optimizer: Adam(lr=1e-4)

    - Loss: Dice Loss

        - L(y, y_hat) = 1 - 2 * |y ∩ y_hat| / |y| + |y_hat| # Intersection over Union

    - Use sigmoid activation function on the prediction

        - Threshold at 0.5 to obtain binary masks.

            - Predictions > 0.5 -> 1 (Left Atrium)
            - Predictions <= 0.5 -> 0 (Not Left Atrium)

    - Train for 75 epochs

        - Save the model with the best validation loss.