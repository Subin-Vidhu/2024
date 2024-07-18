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

    - Optimizer

        - Adam(lr=1e-4)

    - Loss

        - Binary Cross Entropy

    - 100 epochs

- Oversampling

    ```python
    from pathlib import Path
    import numpy as np
    import torch
    from dataset import LungDataset

    # Load the dataset
    train_dataset = LungDataset(Path('Preprocessed/train'), None)

    # Compute the fraction of tumor free slices
    target_list = []
    for _,label in train_dataset:
        if np.any(label):
            target_list.append(1)
        else:
            target_list.append(0)

    unique, counts = np.unique(target_list, return_counts=True)
    fraction = counts[0]/counts[1] 
    print(f"Fraction: {fraction}")

    weight_list = []
    for i in target_list:
        if i == 1:
            weight_list.append(fraction)
        else:
            weight_list.append(1)

    sampler = torch.utils.data.sampler.WeightedRandomSampler(weight_list, len(weight_list)) # WeightedRandomSampler is used to oversample the minority class - in this case the tumor slices
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, sampler=sampler) # DataLoader is used to load the data in batches, here sampler means that the data is loaded in a way that the tumor slices are oversampled so that the network does not predict everything as tumor free

    for data, label in train_loader:
        #print(data.shape, label.shape)
        print(label.sum([1,2,3]) # this means that the label is a 4D tensor and we sum over the last 3 dimensions to get the number of tumor pixels in each slice - each dimension corresponds to a different axis, and if we sum over all of them we get the total number of tumor pixels in each slice
    ``` 

