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
            self.layer1 = DoubleConv(1, 64)
            self.layer2 = DoubleConv(64, 128)
            self.layer3 = DoubleConv(128, 256)
            self.layer4 = DoubleConv(256, 512) # completes the encoder part

            self.layer5 = DoubleConv(512+256, 256)
            self.layer6 = DoubleConv(256+128, 128)
            self.layer7 = DoubleConv(128+64, 64)
            self.layer8 = torch.nn.Conv2d(64, 1, kernel_size=1) # completes the decoder part

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
    x = torch.randn(1, 1, 256, 256, 256)
    # pass it through the model
    y = model(x)
    print(y.shape) # torch.Size([1, 1, 256, 256])
    ```

