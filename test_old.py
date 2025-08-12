# -*- coding: utf-8 -*-
"""
Created on Wed May  7 09:06:43 2025

@author: Aus
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import segmentation_models as sm
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger
from tensorflow.keras.utils import Sequence
import datetime
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
def print_with_timestamp(message):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{current_time}] {message}")
sm.set_framework('tf.keras')

# Check for GPU availability
# gpus = tf.config.experimental.list_physical_devices('GPU')
# print("Physical GPUs:", gpus)
# if gpus:
#     try:
#         # Set GPU memory growth to avoid memory allocation issues
#         # for8 gpu in gpus:
#         #     tf.config.experimental.set_memory_growth(gpu, True)
        
#         # Use all available GPUs for training
#         # Create a MirroredStrategy.
#         strategy = tf.distribute.MirroredStrategy()
#         # strategy = tf.distribute.MirroredStrategy(devices=["/gpu:0", "/gpu:1", "/gpu:2"])  # Update device names as needed
#         print('Number of devices: {}'.format(strategy.num_replicas_in_sync))

# Define the directory where your batch files are saved
batch_directory = 'D:/PROTOS/AIRA/Numpy_Arrays/ALL/FDA/'
num_batches = 7 # Assuming you have 6 batches
# Load entire dataset
all_images = []
all_masks = []
for batch_idx in range(num_batches):
    print_with_timestamp(f"Batch {batch_idx} ...")
    image_batch_filename = f'windowing_improved_06122025_image_batch_{batch_idx}.npy'
    mask_batch_filename = f'windowing_improved_06122025_mask_batch_{batch_idx}.npy'
    image_batch_path = os.path.join(batch_directory, image_batch_filename)
    mask_batch_path = os.path.join(batch_directory, mask_batch_filename)
    image_batch_data = np.load(image_batch_path)
    mask_batch_data = np.load(mask_batch_path)
    all_images.append(image_batch_data)
    all_masks.append(mask_batch_data)
print_with_timestamp("All Data Loaded...")
ground_truth_array = np.concatenate(all_images, axis=0)
mask_array = np.concatenate(all_masks, axis=0)

# Delete unnecessary variables
del all_images, all_masks
print_with_timestamp("All Data Concatenated...")
import random

# Perform sanity check on a random subset of 100 images
sanity_check_indices = random.sample(range(len(ground_truth_array)), 1000)

for idx in sanity_check_indices:
    plt.figure(figsize=(12, 8))
    plt.subplot(231)
    plt.title(f'Ground truth Image {idx}')
    plt.imshow(ground_truth_array[idx,:,:], cmap='gray')
    plt.subplot(232)
    plt.title(f'Mask Image {idx}')
    plt.imshow(mask_array[idx,:,:], cmap='jet')
    plt.show()
    
# Split data into train, validation, and test sets
x_train_val, x_test, y_train_val, y_test = train_test_split(ground_truth_array, mask_array, test_size=0.05, random_state=42)

# Delete unnecessary variables
del ground_truth_array, mask_array

x_train, x_val, y_train, y_val = train_test_split(x_train_val, y_train_val, test_size=0.05, random_state=42)

# Delete unnecessary variables
del x_train_val, y_train_val
print_with_timestamp("Data splitted...")
n_classes = 4
train_masks_cat = to_categorical(y_train, num_classes=n_classes)
y_train_cat = train_masks_cat.reshape((y_train.shape[0], y_train.shape[1], y_train.shape[2], n_classes))

val_masks_cat = to_categorical(y_val, num_classes=n_classes)
y_val_cat = val_masks_cat.reshape((y_val.shape[0], y_val.shape[1], y_val.shape[2], n_classes))

test_masks_cat = to_categorical(y_test, num_classes=n_classes)
y_test_cat = test_masks_cat.reshape((y_test.shape[0], y_test.shape[1], y_test.shape[2], n_classes))

# Delete unnecessary variables
del y_train, y_val, train_masks_cat, val_masks_cat, test_masks_cat
print_with_timestamp("Categorical done...")
activation = 'softmax'
LR = 0.0001
optim = tf.keras.optimizers.Adam(LR)

dice_loss = sm.losses.DiceLoss(class_weights=np.array([0.2, 0.5, 0.35, 0.35]))
focal_loss = sm.losses.CategoricalFocalLoss()
total_loss = dice_loss + (1 * focal_loss)

metrics = ['accuracy', sm.metrics.IOUScore(threshold=0.5), sm.metrics.FScore(threshold=0.5)]

BACKBONE1 = 'resnet101'
preprocess_input1 = sm.get_preprocessing(BACKBONE1)

X_train1 = preprocess_input1(x_train)
X_val1 = preprocess_input1(x_val)
X_test1 = preprocess_input1(x_test)

# Delete unnecessary variables
del x_train, x_val, x_test
print_with_timestamp("Preprocessed...")

# Define DataGenerator class
class DataGenerator(Sequence):
    def __init__(self, x_set, y_set, batch_size):
        self.x, self.y = x_set, y_set
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.x[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size:(idx + 1) * self.batch_size]
        return batch_x, batch_y
    

# with strategy.scope():
model1 = sm.Unet(BACKBONE1, encoder_weights=None, input_shape=(None, None, X_train1.shape[-1]), classes=n_classes, activation=activation)
model1.compile(optim, total_loss, metrics=metrics)

# checkpoint = ModelCheckpoint('D:/PROTOS/AIRA/Results/model_checkpoint.h5', monitor='loss', verbose=1, save_best_only=True, mode='min')
# early_stop = EarlyStopping(monitor='loss', patience=100, verbose=1)
# log_csv = CSVLogger('D:/PROTOS/AIRA/Results/training_logs.csv', separator=',', append=False)
# callbacks_list = [checkpoint, early_stop, log_csv]
# Define callbacks for saving models and logging
checkpoint = ModelCheckpoint('D:/PROTOS/AIRA/Results_FDA/model_checkpoint_{epoch:02d}_{val_loss:.2f}.h5', monitor='loss', verbose=1, save_best_only=False, mode='min')
early_stop = EarlyStopping(monitor='loss', patience=100, verbose=1)
log_csv = CSVLogger('D:/PROTOS/AIRA/Results_FDA/training_logs.csv', separator=',', append=False)
callbacks_list = [checkpoint, early_stop, log_csv]

print(model1.summary())
with open('model_summary.txt', 'w') as f:
    model1.summary(print_fn=lambda x: f.write(x + '\n'))
    
print_with_timestamp("Going to Train...")

try:
    train_gen = DataGenerator(X_train1, y_train_cat, 4)
    history = model1.fit(train_gen, epochs=1000, validation_data=(X_val1, y_val_cat), callbacks=callbacks_list)
except tf.errors.ResourceExhaustedError:
    print("ResourceExhaustedError occurred. Trying with reduced batch size...")
    for bs in [2, 1]:
        try:
            train_gen = DataGenerator(X_train1, y_train_cat, bs)
            history = model1.fit(train_gen, epochs=1000, validation_data=(X_val1, y_val_cat), callbacks=callbacks_list)
            break
        except tf.errors.ResourceExhaustedError:
            continue
    else:
        print("Unable to train even with reduced batch size. Exiting.")
