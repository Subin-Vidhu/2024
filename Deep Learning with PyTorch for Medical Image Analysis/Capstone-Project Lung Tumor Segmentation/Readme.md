### Lung Tumor Segmentation

- Medical Background

    - Lung Cancer / Bronchial Carcinoma is one of the most common cancer worldwide.

        - Makes up 25% of all cancer deaths.

    - Automatic tumor segmentation has 2 advantages:

        - Reduce the probability of missing a tumor.[False Negative]

        - Directly obtain the size/volume of the tumor.

- Dataset    

    - Medical Segmentation Decathlon dataset [link](http://medicaldecathlon.com/dataaws/#:~:text=Task05_Prostate-,Task06_Lung,-Task07_Pancreas)

    - 64 full body CT scans and their ground truth segmentation masks.

        - 31534 2D CT and label slices

        - Problem: Large scan vs relatively small tumor(Imbalance)

- Preprocessing

    - Two dimensional setting. Extract slices!

    - Original size: 512x512

    - Crop away tissue below the lungs

        - 30 pixel along the last axis

        - Also for the label/segmentation mask

    - Standardize with a factor of 1/3071 or try out different windows

    - Resize the single slice to 256x256[use nearest neighbor interpolation - is the method where the value of a pixel in the output image is determined by the value of the pixel at the corresponding position in the input image]

        - [Link](https://annmay10.medium.com/resizing-images-using-various-interpolation-techniques-4b99800999f2)

        - [Link](https://gist.github.com/georgeblck/e3e0274d725c858ba98b1c36c14e2835)

    - Use the last 6 subjects as validation set

- Dataset and Model

    - Use the same dataset and model as in the atrium segmentation

- Training

    - Oversampling

        - Compute the fraction f between tumor free and tumorous slices

        - Sample slices with tumor f times more often

        - Prevents the network from predicting everything as tumor free

    