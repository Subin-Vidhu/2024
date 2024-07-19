### 3D Liver and Liver Tumor Segmentation

- Medical Background

    - Liver cancer is the 6th most common cancer worldwide.
    
        - Makes up 4.7% of all cancer deaths.
        
    - Automatic tumor segmentation has 2 advantages:
    
        - Reduce the probability of missing a tumor.[False Negative]
        
        - Directly obtain the size/volume of the tumor.

- Dataset

    - Medical Segmentation Decathlon dataset [link](http://medicaldecathlon.com/dataaws/#:~:text=Task03_Liver,-Task04_Hippocampus)
    
    - 131 contrast-enhanced CT scans and their ground truth segmentation masks.
    
        - 131 3D CT and label volumes
        
        - Problem: Large scan vs relatively small tumor(Imbalance)    

- Data

    ```python
    %matplotlib inline
    from pathlib import Path
    import nibabel as nib
    import matplotlib.pyplot as plt
    import numpy as np
    from celluloid import Camera
    from IPython.display import HTML

    # Load the data
    root = Path("Task03_Liver_rs/imagesTr/")
    label = Path("Task03_Liver_rs/labelsTr/")

    def change_img_to_label_path(img_path):
        parts = list(img_path.parts)
        parts[parts.index("imagesTr")] = "labelsTr"
        return Path(*parts)

    sample_path = list(root.glob("liver*"))[0]
    sample_path_label = change_img_to_label_path(sample_path)

    ct = nib.load(sample_path).get_fdata() # Load the CT scan
    label = nib.load(sample_path_label).get_fdata().astype(int) # Load the label, cast to int

    print(f"CT shape: {ct.shape}") # (256, 256, 42)