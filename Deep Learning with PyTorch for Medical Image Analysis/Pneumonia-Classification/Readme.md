### Identify signs of pneumonia in chest X-ray images

- Medical background

    - Pneumonia is an infection in one or both lungs. Bacteria, viruses, and other germs cause the lungs' air sacs to become inflamed and filled with fluid or pus. This can make it difficult for the patient to breathe. Pneumonia can range in seriousness from mild to life-threatening. It is most serious for infants and young children, people older than age 65, and people with health problems or weakened immune systems.
 
    - Common infectious disease

    - Symptoms: cough, fever, chills, and difficulty breathing

    - Diagnosis: chest X-ray, blood tests, and sputum tests

- Data

    - Will be using the data from RSNA Pneumonia Detection Challenge on Kaggle. 

    - 26684 chest X-ray images (JPEG) with 1 or more areas of pneumonia

        - 20672 images without pneumonia

        - 6012 images with pneumonia

- Preprocessing

    - Original image size: 1024 x 1024

        - Resized image size: 224 x 224

    - Standardize the pixel values into the interval [0, 1] by scaling with 1/255

    - Split dataset into 24000 training images and 2684 validation images

    - Store converted images in folders corresponding to their classes

        - 0 if no pneumonia

        - 1 if pneumonia

    - Compute training mean and standard deviation for normalization

        - Dataset does not fit into the memory -> Use a trick to compute mean and standard deviation

            - Compute ∑x and ∑x^2 for each image X and add those values to the global variables sums and squared_sums

            - μ = ∑x / N, (sums / N)

            - σ = sqrt(∑x^2 / N - μ^2), sqrt(squared_sums / N - μ^2)

- Dataset

    - Make use of `torchvision.DatasetFolder` to load images from the folders

        - No need for custom dataset class

    - Z- score normalization

        - Normalize the pixel values by subtracting the mean and dividing by the standard deviation

            - X_normalized = (X - μ) / σ

    - Apply data augmentation:

        - Random Rotations

        - Random Translations

        - Random Scales

        - Random resized crops

- Training    

    - Pytorch-lightning

        - High-level pytorch wrapper for simple and effective training

            - No manual implementation of training loop needed

            - Automatically handles multi-GPU training

            - Simple logging and callback interfaces

            - Full access to all variables and parameters

    - Network Architecture

        - ResNet-18

            - Pre-trained on ImageNet

            - Change the input channels from 3 to 1 (because the medical images are not RGB but grayscale)

            - Change the output dimension from 1000 to 1

    - Loss function
