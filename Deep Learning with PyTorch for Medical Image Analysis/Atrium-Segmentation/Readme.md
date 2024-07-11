### Atrium Segmentation

- **Task**: Automatically segment the left atrium in cardiac MR images.

- Medical Background

    - Atrium Segmentation classifies each voxel in the MRI into either "Not Left Atrium" or "Left Atrium".

    - Enables exact volume measurements of the left atrium.

    - Changes in atrial volume are associated with cardiac disorders, sucha s atrial fibrillation or mitral valve stenosis(Narrowing of the mitral valve orifice, blocking blood flow).

    - Manual segmentation is time-consuming and tedious - Automation is needed.

- Data

    - Medical Segmentation Decathlon dataset[Link](http://medicaldecathlon.com/dataaws/)

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
                <img src="image.png" width="200" height="200">

    - Loss Function: Binary Cross-Entropy

    - Optimizer: Adam

    - Training

        - Batch size: 16
        - Learning rate: 0.001
        - Epochs: 100
        - Early stopping: Stop training if validation loss does not improve for 10 epochs.

    - Evaluation

        - Dice Coefficient: 0.85
        - Jaccard Index: 0.74