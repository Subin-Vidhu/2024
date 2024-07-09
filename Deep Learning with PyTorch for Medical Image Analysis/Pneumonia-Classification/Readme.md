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

        - Binary Cross-Entropy with Logits loss

            - This loss is directly applied to the logits or in other words raw predictions by neural networks.


            - negative logits means that the network did not see any sign of pneumonia in the image

            - positive logits means that the network saw some signs of pneumonia in the image

    - Optimizer

        - Adam

            - Adaptive moment estimation

            - Combines the advantages of two other extensions of stochastic gradient descent

                - Adaptive Gradient Algorithm (AdaGrad)

                - Root Mean Square Propagation (RMSProp)

    - Epochs

        - 30

- Interpretability

    - Why does our model output "Pneumonia" for a given image?

        - Find out by extracting the image region with the largeset influence on the prediciton.

            - Which part of the image supports the classifier the most in its prediction?
        
        - Compute Class Activation Maps (CAMs) 

            - Produces a heatmap highlighting the important regions in the image for the classifier's decision

            - Class Activation Map

                - Extract output A(features) with k filters of the last convolutional layer

                - Extract weights w of the fully connected layer

                - Compute the dot product of A and w

                    - M = Σk(w_k * A_k)

                        ![alt text](image.png)

            - Restrictions

                - Only works with CNNs

                - Needs specific structure: Convolution -> Global Average Pooling -> Fully Connected

                    - Only works on networks with single fully connected layer

            - Alternatives

                - Grad-CAM

                    - Gradient-weighted Class Activation Mapping

                    - Works with any differentiable model

                    - Produces similar results to CAM

                - Grad-CAM++

                    - Improved version of Grad-CAM

                    - Produces better visualizations

                - Score-CAM

                    - Score-weighted Class Activation Mapping

                    - Uses the output score to weight the importance of each feature map

                    - Produces better visualizations

- Code

    ```python
    from pathlib import Path
    import pydicom
    import numpy as np
    import cv2
    import pandas as pd
    import matplotlib.pyplot as plt
    from tqdm.notebook import tqdm

    labels = pd.read_csv('stage_2_train_labels.csv')
    labels.head(6) # Display the first 6 rows of the dataframe

    labels = labels.drop_duplicates("patiendID")
    ROOT_PATH = Path("stage_2_train_images/")
    SAVE_PATH = Path("Processed")

    fig, axis = plt.subplots(1, 2, figsize=(10, 5))
    c = 0
    for i in range(3):
        for j in range(3):
            patientId = labels.patientId.iloc[c]
            dcm_path = ROOT_PATH / patientId
            dcm_path = dcm_path.with_suffix(".dcm") # Change the extension to .dcm
            dcm_data = pydicom.read_file(dcm_path).pixel_array

            label = labels["Target"].iloc[c]

            axis[i][j].imshow(dcm_data, cmap="bone")
            axis[i][j].set_title(f"Label: {label}")
            axis[i][j].axis("off")
            c += 1


    # Preprocessing

    sums, sums_squared = 0, 0

    for c, patient_id in enumerate(tqdm(labels.patientId)):
        patient_id = labels.patientId.iloc[c]
        dcm_path = ROOT_PATH / patient_id
        dcm_path = dcm_path.with_suffix(".dcm")
        dcm_data = pydicom.read_file(dcm_path).pixel_array/255 # Scale the pixel values to [0, 1]

        dcm_array = cv2.resize(dcm_data, (224, 224)).astype(np.float16) # Resize the image to 224 x 224

        label = labels["Target"].iloc[c]

        train_or_val = "train" if c < 24000 else "val"

        current_save_path = SAVE_PATH / train_or_val / str(label) / f"{patient_id}.npy"
        current_save_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(current_save_path, dcm_array)

        normalized_dcm_data = 224*224
        
        if train_or_val == "train":
            sums += np.sum(dcm_array)/normalizer
            sums_squared += np.sum(dcm_array**2)/normalizer

        mean = sums/24000
        std = np.sqrt(sums_squared/24000 - mean**2)
        print(f"Mean: {mean}, Std: {std}") # Mean: 0.482, Std: 0.229


    # Training
    import torch
    import torchvison
    from torchvision import transforms
    import torch_metrics
    import pytorch_lightning as pl
    from pytorch_lightning.callbacks import ModelCheckpoint
    from pytorch_lightning.loggers import TensorBoardLogger
    from tqdm.notebook import tqdm
    import numpy as np
    import matplotlib.pyplot as plt

    def load_file(file_path):
        return np.load(file_path).astype(np.float32) # Load the numpy file and convert it to float32
        
    train_transform = transforms.Compose([
        transforms.ToTensor(), # Convert the image to a tensor
        transforms.Normalize(mean=[0.482], std=[0.229]),  # Normalize the pixel values from the mean and standard deviation obtained earlier
        transforms.RandomAffine(degrees=(-5, 5), translate=(0, 0.05), scale=(0.9, 1.1)), # Apply random rotations, translations, and scales to the image so that the model can learn from different perspectives
        transforms.RandomResizedCrop((224, 224), scale=(0.35, 1)), # Apply random resized crops to the image
       
    ])

    val_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.482], std=[0.229]),
    ]) # here we are not applying any data augmentation to the validation images because we want to evaluate the model on the original images

    train_dataset = torchvision.datasets.DatasetFolder("Processed/train", loader=load_file, extensions=(".npy"), transform=train_transform)

    val_dataset = torchvision.datasets.DatasetFolder("Processed/val", loader=load_file, extensions=(".npy"), transform=val_transform)

    fig, axis = plt.subplots(1, 2, figsize=(10, 5))
    for i in range(2):
        for j in range(2):
            randon_index = np.random.randint(0, len(train_dataset))
            x_ray, label = train_dataset[randon_index]
            axis[i][j].imshow(x_ray[0], cmap="bone") #[0] is used to remove the channel dimension otherwise the image will not be displayed and will be ended up with an error
            axis[i][j].set_title(f"Label: {label}")
            

    # Define batch_size and num_workers based on the available resources
    batch_size = 64
    num_workers = 4

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers) # shuffle the training data is important to prevent the model from memorizing the order of the images
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers) # shuffle the validation data is not necessary because we are not training the model on it

    # To check how many images actually show signs of pneumonia
    np.unique(train_dataset.targets, return_counts=True) # (array([0, 1]), array([18593, 5407])) - imbalance dataset as there are more images without pneumonia than with pneumonia

    # Methods to overcome class imbalance
    # 1. To do Nothing - Let the model learn from the imbalanced dataset
    # 2. Weighted Loss - Assign higher loss to a prediction if the model gets it wrong for the minority class
    # 3. Oversampling - Duplicate the minority class samples to balance the dataset, here 3 times the minority class samples are duplicated

    # Define the model - model creation
    # to display the details of a model
    torchvision.models.resnet18() # ResNet-18 model- 18 layers deep, prints out the data of each layer

    class PneumoniaClassifier(pl.LightningModule):
        def __init__(self):
            super().__init__()
            self.resnet = torchvision.models.resnet18(pretrained=True) # Load the pre-trained ResNet-18 model to use the pre-trained weights
            self.resnet.conv1 = torch.nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False) # Change the input channels from 3 to 1 as we are using grayscale images
            self.resnet.fc = torch.nn.Linear(in_features=512, out_features=1, bias=True) # Change the output dimension from 1000 to 1 as our task is binary classification
            self.optimizer = torch.optim.Adam(self.model.parameters(), lr = 1e-4) # Define the optimizer
            self.loss_fn = torch.nn.BCEWithLogitsLoss(pos_weight = torch.tensor([3])) # Define the loss function - Binary Cross-Entropy with Logits loss , pos_weight is used to assign higher loss to a prediction if the model gets it wrong for the minority class
            self.train_accuracy = torchmetrics.Accuracy() # Define the training accuracy metric
            self.val_accuracy = torchmetrics.Accuracy() # Define the validation accuracy metric


        def forward(self, data):
            return self.model(data) 

        def training_step(self, batch, batch_idx):
            x_ray, label = batch
            label = label.float() # Convert the label to float
            pred = self(x_ray)[:,0] # Get the predictions from the model, [:,0] is used to remove the channel dimension
            loss = self.loss_fn(pred, label) # Compute the loss
            self.log("train_loss", loss) # Log the training loss
            self.log("train_accuracy", self.train_accuracy(torch.sigmoid(pred), label.int())) # Log the training accuracy
            return loss

        def training_epoch_end(self, outputs):
            self.log("train_accuracy_epoch", self.train_accuracy.compute()) # Log the training accuracy at the end of the epoch

        # Validation step - similar to the training step, but we are not computing the gradients, hence no need to return the loss
        def validation_step(self, batch, batch_idx):
            x_ray, label = batch
            label = label.float()
            pred = self(x_ray)[:,0]
            loss = self.loss_fn(pred, label)
            self.log("val_loss", loss)
            self.log("val_accuracy", self.val_accuracy(torch.sigmoid(pred), label.int()))

        def validation_epoch_end(self, outputs):
            self.log("val_accuracy_epoch", self.val_accuracy.compute())

        def configure_optimizers(self):
            return [self.optimizer] # Return the optimizer to be used for training
 

    # Training the model
    model = PneumoniaClassifier()
    # Define the checkpoint callback to save the best model based on the validation accuracy
    checkpoint_callback = ModelCheckpoint(monitor="val_accuracy_epoch", save_top_k=10, mode="max") # Save the top 10 models based on the validation accuracy

    gpus = 1 # Number of GPUs to use for training - make sure to have the required hardware to use multiple GPUs
    trainer = pl.Trainer(max_epochs=30, gpus=gpus, callbacks=[checkpoint_callback], logger=TensorBoardLogger(save_dir = "./logs", name="Pneumonia_Classifier"), log_every_n_steps = 1) # Define the trainer - max_epochs is the number of epochs to train the model, log_every_n_steps is the number of steps after which the logs are updated, TensorBoardLogger is used to log the training and validation metrics - logs are saved in the logs directory

    trainer.fit(model, train_loader, val_loader) # Fit the model to the training data

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # Check if GPU is available, if not use CPU

    model = PneumoniaModel.load_from_checkpoint("path_to_checkpoint") # Load the best model from the checkpoint
    model.eval() # Set the model to evaluation mode
    model.to(device) # Move the model to the device


    preds = []
    labels = []
    with torch.no_grad():
        for data, label in tqdm(val_dataset):
            data = data.to(device).float().unsqueeze(0) # Convert the data to float and add a batch dimension
            pred = torch.sigmoid(model(data)[0].cpu()) # Get the prediction from the model and convert it to the CPU, [0] is used to remove the batch dimension
            preds.append(pred) # Append the prediction to the list
            labels.append(label) # Append the label to the list
    
    preds = torch.tensor(preds)
    labels = torch.tensor(labels).int() # convert both to tensor so that we can use torch metrics

    acc = torchmetrics.Accuracy()(preds, labels) # Compute the accuracy
    print(f"Accuracy: {acc}") # Accuracy: 0.85
    precision = torchmetrics.Precision()(preds, labels) # Compute the precision
    print(f"Precision: {precision}") # Precision: 0.75
    recall = torchmetrics.Recall()(preds, labels) # Compute the recall
    print(f"Recall: {recall}") # Recall: 0.65

    confusion_matrix = torchmetrics.ConfusionMatrix(num_classes = 2)(preds, labels) # Compute the confusion matrix
    print(f"Confusion Matrix: {confusion_matrix}") # Confusion Matrix: tensor([[2000,  300], [ 400,  984]])
         
    # Interpretability