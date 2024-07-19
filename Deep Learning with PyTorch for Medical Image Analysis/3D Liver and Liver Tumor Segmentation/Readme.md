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

    # Plot the data
    fig = plt.figure(figsize=(10, 10))
    camera = Camera(fig)

    for i in range(ct.shape[2]):
        plt.imshow(ct[:,:,i], cmap="gray")
        mask_ = np.ma.masked_where(label[:,:,i] == 0, label[:,:,i]) # Mask the background
        plt.imshow(mask_, cmap="cool", alpha=0.5)
        plt.axis("off")
        camera.snap()

    animation = camera.animate(interval=100)

    HTML(animation.to_html5_video())
    ```

- Model

    - U-Net
    
        - Encoder: Convolutional layers with max pooling
        
        - Decoder: Convolutional layers with up-sampling
        
        - Skip connections: Concatenate the output of the encoder with the input of the decoder
        
        - Output: Sigmoid activation function
        
    - Loss: Binary Cross Entropy
    
    - Optimizer: Adam(lr=1e-4)

    ```python
    # To convert the 2D U-Net to 3D U-Net, we need to change the Conv2d and MaxPool2d layers to Conv3d and MaxPool3d layers, respectively, and now since we have volumes instead of slices, we need to use trilinear upsampling instead of bilinear upsampling, and increase the output channels from 1 to 3
    import torch
    class DoubleConv(torch.nn.module):
        def __init__(self, in_channels, out_channels):
            super().__init__()
            self.step = torch.nn.Sequential(
                torch.nn.Conv3d(in_channels, out_channels, kernel_size=3, padding=1),
                torch.nn.ReLU(),
                torch.nn.Conv3d(out_channels, out_channels, kernel_size=3, padding=1),
                torch.nn.ReLU()
            )

        def forward(self, x):
            return self.step(x)

    class UNet(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.layer1 = DoubleConv(1, 32)
            self.layer2 = DoubleConv(32, 64)
            self.layer3 = DoubleConv(64, 128)
            self.layer4 = DoubleConv(128, 256) # completes the encoder part

            self.layer5 = DoubleConv(256+128, 128)
            self.layer6 = DoubleConv(128+64, 64)
            self.layer7 = DoubleConv(64+32, 32)
            self.layer8 = torch.nn.Conv3d(32, 3, kernel_size=1) # completes the decoder part

            self.maxpool = torch.nn.MaxPool3d(2)

        def forward(self, x):
            x1 = self.layer1(x)
            x2 = self.layer2(self.maxpool(x1))
            x3 = self.layer3(self.maxpool(x2))
            x4 = self.layer4(self.maxpool(x3)) # completes the encoder part

            x5 = torch.nn.Upsample(scale_factor=2, mode="trilinear", align_corners=True)(x4)
            x5 = torch.cat([x5, x3], dim=1) # Concatenate the feature maps from the encoder with the decoder, dim = 1 is the channel dimension
            x5 = self.layer5(x5)

            x6 = torch.nn.Upsample(scale_factor=2, mode="trilinear", align_corners=True)(x5)
            x6 = torch.cat([x6, x2], dim=1)
            x6 = self.layer6(x6)

            x7 = torch.nn.Upsample(scale_factor=2, mode="trilinear", align_corners=True)(x6)
            x7 = torch.cat([x7, x1], dim=1)
            x7 = self.layer7(x7)

            ret = self.layer8(x7)
            return ret

    model = UNet()
    # create a random input
    x = torch.randn(1, 1, 128, 128, 128)
    # pass it through the modelfrom pathlib import Path
    import torch
    import pytorch_lightning as pl
    import pytorch_lightning.callbacks import ModelCheckpoint
    from pytorch_lightning.loggers import TensorBoardLogger
    import imgaug.augmenters as iaa
    import cv2
    import matplotlib.pyplot as plt

    from dataset import CardiacDataset
    from model import UNet
    y = model(x)
    print(y.shape) # torch.Size([1, 3, 128, 128,128])
    # create a new model.py file with the UNet class and the DoubleConv class so that import it in the main script
    ```

- Train

    ```python
    from pathlib import Path
    import torch
    import torchio as tio
    import pytorch_lightning as pl
    import pytorch_lightning.callbacks import ModelCheckpoint
    from pytorch_lightning.loggers import TensorBoardLogger
    from model import UNet

    def change_img_to_label_path(img_path):
        parts = list(img_path.parts)
        parts[parts.index("imagesTr")] = "labelsTr"
        return Path(*parts)    

    path = Path("Task03_Liver_rs/imagesTr/")
    subject_paths = list(path.glob("liver_*"))
    subjects = []
    for subject_path in subject_paths:
        label_path = change_img_to_label_path(subject_path)
        subject = tio.Subject({
            "CT"=tio.ScalarImage(subject_path),
            "Label"=tio.LabelMap(label_path)
        })
        subjects.append(subject)

    for subject in subjects:
        assert subject["CT"].orientation == ("R", "A", "S")

    process = tio.Compose([tio.crop_or_pad((256, 256, 100)), tio.RescaleIntensity((-1, 1))])

    augmentation = tio.RandomAffine(scales=(0.9, 1.1), degrees=(-10, 10))

    val_transform = process
    train_transform = tio.Compose([process, augmentation])

    # Lets use the first 105 for training and remaining for validation
    train_dataset = tio.SubjectsDataset(subjects[:105], transform=train_transform)
    val_dataset = tio.SubjectsDataset(subjects[105:], transform=val_transform)

    sampler = tio.data.LabelSampler(patch_size = 96, label_name = "Label", label_prob = {0: 0.2, 1: 0.3, 2: 0.5})

    train_patches_queue = tio.Queue(
        subjects_dataset=train_dataset,
        max_length=40,
        samples_per_volume=5,
        sampler=sampler,
        num_workers=4
    ) # this is done to create patches from the volumes, detailed explanation is that the volumes are too large to fit in the memory, so we create patches of the volumes and then train the network on these patches, here we are creating 5 patches per volume and the maximum length of the queue is 40, so that we can have 40 patches in the queue at a time, queue is used to load the data in parallel. So what happens here is that the queue will load the data in parallel and create patches from the volumes and then the network will be trained on these patches. So at a time we have 40 patches in the queue and the queue will keep on loading the data in parallel and creating patches from the volumes and the network will keep on training on these patches.

    val_patches_queue = tio.Queue(
        subjects_dataset=val_dataset,
        max_length=40,
        samples_per_volume=5,
        sampler=sampler,
        num_workers=4
    )

    train_loader = torch.utils.data.DataLoader(train_patches_queue, batch_size=2, num_workers=0)
    val_loader = torch.utils.data.DataLoader(val_patches_queue, batch_size=2, num_workers=0 # DataLoader is used to load the data in batches, here we are loading the data in batches of 2, and we are using 0 workers, this is because we are using the queue to load the data in parallel, so we do not need to use the workers here

    ```
