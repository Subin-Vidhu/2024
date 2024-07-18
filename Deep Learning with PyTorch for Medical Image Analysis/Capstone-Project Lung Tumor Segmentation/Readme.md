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

        