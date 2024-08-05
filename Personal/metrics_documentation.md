
# Metrics Documentation

## General Information

#### Explanation of y_test and y_pred_argmax Values

`y_test`: This is the ground truth or actual labels for your data. Each value represents the class of a pixel in the image.

`y_pred_argmax`: This is the predicted label for each pixel from your model. Each value is the class that your model predicts for a given pixel.
In a multi-class segmentation task:

The values in y_test and y_pred_argmax should be integers representing class labels (e.g., 0, 1, 2 for a 3-class problem).

The dimensions of y_test and y_pred_argmax should match the number of images and the resolution of each image (height, width).

#### Code to Create Random Values
```python
import tensorflow as tf
from tensorflow.keras.metrics import MeanIoU, Precision, Recall, Accuracy
import numpy as np
from sklearn.metrics import cohen_kappa_score

# Parameters
num_test_images = 10
image_height = 256
image_width = 256
num_classes = 3

# Create random ground truth labels (ground_truth_labels)
ground_truth_labels = np.random.randint(0, num_classes, size=(num_test_images, image_height, image_width, 1))

# Create random predicted labels (predicted_class_indices)
predicted_class_indices = np.random.randint(0, num_classes, size=(num_test_images, image_height, image_width, 1))

# Convert to appropriate tensor format and cast to int32
ground_truth_labels_tensor = tf.cast(tf.convert_to_tensor(ground_truth_labels), tf.int32)
predicted_class_indices_tensor = tf.cast(tf.convert_to_tensor(predicted_class_indices), tf.int32)

# in real-world scenarios, you would have your own ground truth and predicted values
# Predict the output of the model
# y_pred = model.predict(X_test)
# y_pred_argmax = np.argmax(y_pred, axis=3)

# Ensure predicted_class_indices has the same shape as ground_truth_labels
if len(predicted_class_indices_tensor.shape) < len(ground_truth_labels_tensor.shape):
    predicted_class_indices_tensor = tf.expand_dims(predicted_class_indices_tensor, axis=-1) # Add channel dimension if missing
```

## Pixel Accuracy
**Definition**: Pixel accuracy is the proportion of correctly classified pixels to the total number of pixels.

**Formula**: 

$$
\text{Pixel Accuracy} = \frac{\sum\limits_{i=1}^{n} \mathbf{1}(y_i = \hat{y}_i)}{n}
$$

**Example**: If 95 out of 100 pixels are correctly classified, the pixel accuracy is 95%.

**Code**:
```python
pixel_accuracy_metric = Accuracy()
pixel_accuracy_metric.update_state(ground_truth_labels_tensor, predicted_class_indices_tensor)
pixel_accuracy = pixel_accuracy_metric.result().numpy()
print(f"Pixel Accuracy: {pixel_accuracy}")
```

## Mean Intersection over Union (Mean IoU)
**Definition**: IoU is the ratio of the intersection of the predicted and ground truth masks to their union. Mean IoU is the average IoU across all classes.

**Formula**: 

$$
\text{IoU} = \frac{|A \cap B|}{|A \cup B|}
$$

**Example**: If the intersection is 30 pixels and the union is 50 pixels, IoU = 0.6. Mean IoU averages this value across all classes.

**Code**:
```python
iou_metric = MeanIoU(num_classes=num_classes)
iou_metric.update_state(ground_truth_labels_tensor, predicted_class_indices_tensor)
mean_iou = iou_metric.result().numpy()
print(f"Mean IoU: {mean_iou}")
```

## Class-wise IoU
**Definition**: IoU for each class is calculated individually using the same formula as Mean IoU.

**Formula**: 

$$
\text{IoU} = \frac{|A \cap B|}{|A \cup B|}
$$

**Example**: Calculated per class using the above formula.

**Code**:
```python
iou_values = iou_metric.get_weights()[0]
for class_index in range(num_classes):
    class_iou = iou_values[class_index, class_index] / (np.sum(iou_values[class_index, :]) + np.sum(iou_values[:, class_index]) - iou_values[class_index, class_index])
    print(f"IoU for class {class_index}: {class_iou}")
```

## Dice Coefficient (F1 Score)
**Definition**: The Dice coefficient, also known as the F1 score, is a measure of overlap between two samples.

**Formula**: 

$$
\text{Dice Coefficient} = \frac{2 \cdot |A \cap B|}{|A| + |B|}
$$

**Example**: If the intersection is 20 pixels, and the sum of all pixels in both sets is 40, Dice coefficient = 1.

**Code**:
```python
dice_coefficient = 2 * mean_iou / (1 + mean_iou)
print(f"Dice Coefficient (F1 Score): {dice_coefficient}")

# Class-wise Dice Coefficient
def calculate_dice_coefficient(ground_truth_labels, predicted_class_indices, class_index):
    ground_truth_labels_binary = tf.cast(tf.equal(ground_truth_labels, class_index), tf.float32)
    predicted_class_indices_binary = tf.cast(tf.equal(predicted_class_indices, class_index), tf.float32)
    intersection = tf.reduce_sum(ground_truth_labels_binary * predicted_class_indices_binary)
    return (2 * intersection) / (tf.reduce_sum(ground_truth_labels_binary) + tf.reduce_sum(predicted_class_indices_binary) + 1e-7)

for class_index in range(num_classes):
    dice_coefficient = calculate_dice_coefficient(ground_truth_labels_tensor, predicted_class_indices_tensor, class_index)
    print(f"Dice Coefficient for class {class_index}: {dice_coefficient.numpy()}")
```

## Precision
**Definition**: Precision is the ratio of true positive predictions to the total predicted positives.

**Formula**: 

$$
\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}
$$

**Example**: If there are 80 true positives and 20 false positives, precision = 0.8.

**Code**:
```python
# Class-wise Precision and Recall
for class_index in range(num_classes):
    class_precision_metric = Precision()
    class_mask = tf.equal(ground_truth_labels_tensor, class_index)
    class_predictions = tf.equal(predicted_class_indices_tensor, class_index)
    class_precision_metric.update_state(class_mask, class_predictions)
    class_recall_metric.update_state(class_mask, class_predictions)
    print(f"Class {class_index}:")
    print(f"  Precision: {class_precision_metric.result().numpy()}")
```

## Recall
**Definition**: Recall is the ratio of true positive predictions to the total actual positives.

**Formula**: 

$$
\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}
$$

**Example**: If there are 70 true positives and 30 false negatives, recall = 0.7.

**Code**:
```python
# Class-wise Precision and Recall
for class_index in range(num_classes):
    class_recall_metric = Recall()
    class_mask = tf.equal(ground_truth_labels_tensor, class_index)
    class_predictions = tf.equal(predicted_class_indices_tensor, class_index)
    class_recall_metric.update_state(class_mask, class_predictions)
    print(f"Class {class_index}:")
    print(f"  Recall: {class_recall_metric.result().numpy()}")
```

## Class-wise Precision and Recall
**Definition**: Precision and recall calculated for each class separately.

**Code**:
```python
# Class-wise Precision and Recall
class_precision_metrics = [Precision() for _ in range(num_classes)]
class_recall_metrics = [Recall() for _ in range(num_classes)]

for class_index in range(num_classes):
    class_mask = tf.equal(ground_truth_labels_tensor, class_index)
    class_predictions = tf.equal(predicted_class_indices_tensor, class_index)
    class_precision_metrics[class_index].update_state(class_mask, class_predictions)
    class_recall_metrics[class_index].update_state(class_mask, class_predictions)

print("Precision values for each class:")
for class_index in range(num_classes):
    precision = class_precision_metrics[class_index].result().numpy()
    print(f"Class {class_index}: {precision}")

print("\nRecall values for each class:")
for class_index in range(num_classes):
    recall = class_recall_metrics[class_index].result().numpy()
    print(f"Class {class_index}: {recall}")
    
```

## Cohen's Kappa
**Definition**: Cohen's Kappa is a statistic that measures inter-annotator agreement for categorical items.

**Formula**: 

$$
\kappa = \frac{p_o - p_e}{1 - p_e}
$$

where \( p_o \) is the relative observed agreement and \( p_e \) is the hypothetical probability of chance agreement.

**Example**: If observed agreement is 0.8 and expected agreement is 0.5, Cohen's Kappa = 0.6.

**Code**:
```python
# Cohen's Kappa using scikit-learn
# Flatten the arrays to 1D
ground_truth_labels_flat = tf.reshape(ground_truth_labels_tensor, [-1]).numpy()
predicted_class_indices_flat = tf.reshape(predicted_class_indices_tensor, [-1]).numpy()
cohen_kappa_score_value = cohen_kappa_score(ground_truth_labels_flat, predicted_class_indices_flat)
print(f"Cohen's Kappa: {cohen_kappa_score_value}")
```


### Full Code - Random
```python
import tensorflow as tf
from tensorflow.keras.metrics import MeanIoU, Precision, Recall, Accuracy
import numpy as np
from sklearn.metrics import cohen_kappa_score

# Parameters
num_test_images = 10
image_height = 256
image_width = 256
num_classes = 3

# Create random ground truth labels (ground_truth_labels)
ground_truth_labels = np.random.randint(0, num_classes, size=(num_test_images, image_height, image_width, 1))

# Create random predicted labels (predicted_class_indices)
predicted_class_indices = np.random.randint(0, num_classes, size=(num_test_images, image_height, image_width, 1))

# in real-world scenarios, you would have your own ground truth and predicted values
# Predict the output of the model
# y_pred = model.predict(X_test)
# y_pred_argmax = np.argmax(y_pred, axis=3)

# Convert to appropriate tensor format and cast to int32
ground_truth_labels_tensor = tf.cast(tf.convert_to_tensor(ground_truth_labels), tf.int32)
predicted_class_indices_tensor = tf.cast(tf.convert_to_tensor(predicted_class_indices), tf.int32)

# Ensure predicted_class_indices has the same shape as ground_truth_labels
if len(predicted_class_indices_tensor.shape) < len(ground_truth_labels_tensor.shape):
    predicted_class_indices_tensor = tf.expand_dims(predicted_class_indices_tensor, axis=-1)

# Pixel Accuracy
pixel_accuracy_metric = Accuracy()
pixel_accuracy_metric.update_state(ground_truth_labels_tensor, predicted_class_indices_tensor)
pixel_accuracy = pixel_accuracy_metric.result().numpy()
print(f"\nPixel Accuracy: {pixel_accuracy}")

# IoU and Dice Coefficient (F1 Score)
iou_metric = MeanIoU(num_classes=num_classes)
iou_metric.update_state(ground_truth_labels_tensor, predicted_class_indices_tensor)
mean_iou = iou_metric.result().numpy()
print(f"\nMean IoU: {mean_iou}\n")

# Class-wise IoU
iou_values = iou_metric.get_weights()[0]
for class_index in range(num_classes):
    class_iou = iou_values[class_index, class_index] / (np.sum(iou_values[class_index, :]) + np.sum(iou_values[:, class_index]) - iou_values[class_index, class_index])
    print(f"IoU for class {class_index}: {class_iou}")

# Dice Coefficient (F1 Score)
dice_coefficient = 2 * mean_iou / (1 + mean_iou)
print(f"\nDice Coefficient (F1 Score): {dice_coefficient}\n")

# Class-wise Dice Coefficient
def calculate_dice_coefficient(ground_truth_labels, predicted_class_indices, class_index):
    ground_truth_labels_binary = tf.cast(tf.equal(ground_truth_labels, class_index), tf.float32)
    predicted_class_indices_binary = tf.cast(tf.equal(predicted_class_indices, class_index), tf.float32)
    intersection = tf.reduce_sum(ground_truth_labels_binary * predicted_class_indices_binary)
    return (2 * intersection) / (tf.reduce_sum(ground_truth_labels_binary) + tf.reduce_sum(predicted_class_indices_binary) + 1e-7)

for class_index in range(num_classes):
    dice_coefficient = calculate_dice_coefficient(ground_truth_labels_tensor, predicted_class_indices_tensor, class_index)
    print(f"Dice Coefficient for class {class_index}: {dice_coefficient.numpy()}")


# Class-wise Precision and Recall
class_precision_metrics = [Precision() for _ in range(num_classes)]
class_recall_metrics = [Recall() for _ in range(num_classes)]

for class_index in range(num_classes):
    class_mask = tf.equal(ground_truth_labels_tensor, class_index)
    class_predictions = tf.equal(predicted_class_indices_tensor, class_index)
    class_precision_metrics[class_index].update_state(class_mask, class_predictions)
    class_recall_metrics[class_index].update_state(class_mask, class_predictions)

print("\nPrecision values for each class:")
for class_index in range(num_classes):
    precision = class_precision_metrics[class_index].result().numpy()
    print(f"Class {class_index}: {precision}")

print("\nRecall values for each class:")
for class_index in range(num_classes):
    recall = class_recall_metrics[class_index].result().numpy()
    print(f"Class {class_index}: {recall}")
    
# Cohen's Kappa using scikit-learn
# Flatten the arrays to 1D
ground_truth_labels_flat = tf.reshape(ground_truth_labels_tensor, [-1]).numpy()
predicted_class_indices_flat = tf.reshape(predicted_class_indices_tensor, [-1]).numpy()
cohen_kappa_score_value = cohen_kappa_score(ground_truth_labels_flat, predicted_class_indices_flat)
print(f"\nCohen's Kappa: {cohen_kappa_score_value}")
```

### Full Code - Real Data
```python
import tensorflow as tf
import numpy as np

# Assuming y_test and y_pred_argmax are your ground truth and predicted labels respectively
n_classes = 3  # Adjust this if you have a different number of classes

# Convert to appropriate tensor format if not already
y_test = tf.convert_to_tensor(y_test)
y_pred_argmax = tf.convert_to_tensor(y_pred_argmax)

# Remove the extra dimension from y_test if needed
y_test = tf.squeeze(y_test)

# Pixel Accuracy
accuracy = tf.keras.metrics.Accuracy()
accuracy.update_state(y_test, y_pred_argmax)
pixel_accuracy = accuracy.result().numpy()

# Mean IoU and Confusion Matrix
miou = tf.keras.metrics.MeanIoU(num_classes=n_classes)
miou.update_state(y_test, y_pred_argmax)
mean_iou = miou.result().numpy()
confusion_matrix = miou.total_cm

# Function to calculate IoU
def calculate_iou(y_true, y_pred, class_index):
    y_true_class = tf.cast(tf.equal(y_true, class_index), tf.float32)
    y_pred_class = tf.cast(tf.equal(y_pred, class_index), tf.float32)
    intersection = tf.reduce_sum(y_true_class * y_pred_class)
    union = tf.reduce_sum(y_true_class) + tf.reduce_sum(y_pred_class) - intersection
    return intersection / (union + tf.keras.backend.epsilon())

# Function to calculate Dice Coefficient
def calculate_dice_coefficient(y_true, y_pred, class_index):
    y_true_class = tf.cast(tf.equal(y_true, class_index), tf.float32)
    y_pred_class = tf.cast(tf.equal(y_pred, class_index), tf.float32)
    intersection = tf.reduce_sum(y_true_class * y_pred_class)
    return (2. * intersection) / (tf.reduce_sum(y_true_class) + tf.reduce_sum(y_pred_class) + tf.keras.backend.epsilon())

# Function to calculate Precision
def calculate_precision(y_true, y_pred, class_index):
    y_true_class = tf.cast(tf.equal(y_true, class_index), tf.float32)
    y_pred_class = tf.cast(tf.equal(y_pred, class_index), tf.float32)
    true_positives = tf.reduce_sum(y_true_class * y_pred_class)
    predicted_positives = tf.reduce_sum(y_pred_class)
    return true_positives / (predicted_positives + tf.keras.backend.epsilon())

# Function to calculate Recall
def calculate_recall(y_true, y_pred, class_index):
    y_true_class = tf.cast(tf.equal(y_true, class_index), tf.float32)
    y_pred_class = tf.cast(tf.equal(y_pred, class_index), tf.float32)
    true_positives = tf.reduce_sum(y_true_class * y_pred_class)
    actual_positives = tf.reduce_sum(y_true_class)
    return true_positives / (actual_positives + tf.keras.backend.epsilon())

# Calculate per-class metrics
per_class_metrics = []
for i in range(n_classes):
    iou = calculate_iou(y_test, y_pred_argmax, i)
    dice = calculate_dice_coefficient(y_test, y_pred_argmax, i)
    precision = calculate_precision(y_test, y_pred_argmax, i)
    recall = calculate_recall(y_test, y_pred_argmax, i)
    per_class_metrics.append((iou.numpy(), dice.numpy(), precision.numpy(), recall.numpy()))

# Cohen's Kappa
n = tf.cast(tf.reduce_sum(confusion_matrix), tf.float32)
sum_po = tf.cast(tf.linalg.trace(confusion_matrix), tf.float32)
sum_pe = tf.reduce_sum(tf.cast(tf.reduce_sum(confusion_matrix, axis=0) * tf.reduce_sum(confusion_matrix, axis=1), tf.float32)) / n
po = sum_po / n
pe = sum_pe / n
kappa = (po - pe) / (1 - pe + tf.keras.backend.epsilon())

# Print results
print(f"Pixel Accuracy: {pixel_accuracy}")
print(f"Mean IoU: {mean_iou}")

print("IoU:")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[0]}")

print("Precision:")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[2]}")

print("Recall:")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[3]}")

print("F1 Score (Dice Coefficient):")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[1]}")

print(f"Mean Dice Coefficient (F1 Score): {np.mean([m[1] for m in per_class_metrics])}")
print(f"Cohen's Kappa: {kappa.numpy()}")

# import tensorflow as tf
# import numpy as np

# # Assuming y_test and y_pred_argmax are your ground truth and predicted labels respectively
# n_classes = 3  # Adjust this if you have a different number of classes

# # Convert to appropriate tensor format if not already
# y_test = tf.convert_to_tensor(y_test)
# y_pred_argmax = tf.convert_to_tensor(y_pred_argmax)

# # Remove the extra dimension from y_test if needed
# y_test = tf.squeeze(y_test)

# # Pixel Accuracy
# accuracy = tf.keras.metrics.Accuracy()
# accuracy.update_state(y_test, y_pred_argmax)
# pixel_accuracy = accuracy.result().numpy()

# # IoU
# iou_metric = tf.keras.metrics.MeanIoU(num_classes=n_classes)
# iou_metric.update_state(y_test, y_pred_argmax)
# mean_iou = iou_metric.result().numpy()

# # Get confusion matrix
# iou_values = iou_metric.get_weights()[0]

# # Function to calculate metrics for each class
# def calculate_metrics(confusion_matrix, class_id):
#     true_positives = confusion_matrix[class_id, class_id]
#     false_positives = np.sum(confusion_matrix[:, class_id]) - true_positives
#     false_negatives = np.sum(confusion_matrix[class_id, :]) - true_positives
    
#     iou = true_positives / (true_positives + false_positives + false_negatives + 1e-10)
#     precision = true_positives / (true_positives + false_positives + 1e-10)
#     recall = true_positives / (true_positives + false_negatives + 1e-10)
    
#     return iou, precision, recall

# # Calculate metrics for each class
# class_metrics = [calculate_metrics(iou_values, i) for i in range(n_classes)]

# # Dice Coefficient (F1 Score)
# def dice_coefficient(y_true, y_pred, class_index):
#     y_true_f = tf.cast(tf.equal(y_true, class_index), tf.float32)
#     y_pred_f = tf.cast(tf.equal(y_pred, class_index), tf.float32)
#     intersection = tf.reduce_sum(y_true_f * y_pred_f)
#     return (2 * intersection) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + 1e-7)

# # Cohen's Kappa
# def cohen_kappa(confusion_matrix):
#     n = np.sum(confusion_matrix)
#     sum_po = np.sum(np.diag(confusion_matrix))
#     sum_pe = np.sum(np.sum(confusion_matrix, axis=0) * np.sum(confusion_matrix, axis=1)) / n
#     po = sum_po / n
#     pe = sum_pe / n
#     kappa = (po - pe) / (1 - pe)
#     return kappa

# # Calculate Cohen's Kappa
# kappa = cohen_kappa(iou_values)

# # Print results
# print(f"Pixel Accuracy: {pixel_accuracy}")

# print(f"\nMean IoU: {mean_iou}")

# print("\nIoU:")
# for i, (iou, _, _) in enumerate(class_metrics):
#     print(f"  Class {i}: {iou}")

# print("\nPrecision:")
# for i, (_, precision, _) in enumerate(class_metrics):
#     print(f"  Class {i}: {precision}")

# print("\nRecall:")
# for i, (_, _, recall) in enumerate(class_metrics):
#     print(f"  Class {i}: {recall}")

# print("\nDice Coefficient (F1 Score):")
# dice_scores = []
# for i in range(n_classes):
#     dice = dice_coefficient(y_test, y_pred_argmax, i)
#     dice_scores.append(dice.numpy())
#     print(f"  Class {i}: {dice.numpy()}")

# print(f"\nMean Dice Coefficient (F1 Score): {np.mean(dice_scores)}")

# print(f"\nCohen's Kappa: {kappa}")
```

## Full Code - Real Data Optimized with visualization
```python

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix as sk_confusion_matrix
from sklearn.metrics import roc_curve, auc

# Assuming y_test and y_pred_argmax are your ground truth and predicted labels respectively
n_classes = 3  # Adjust this if you have a different number of classes

# Create temporary arrays for testing
y_test_ = np.random.randint(0, n_classes, size=(100, 100))  # 100x100 array with random class labels
y_pred_argmax_ = np.random.randint(0, n_classes, size=(100, 100))  # 100x100 array with random predicted class labels

# Input validation
def validate_input(y_test, y_pred_argmax):
    if not isinstance(y_test, tf.Tensor) or not isinstance(y_pred_argmax, tf.Tensor):
        raise ValueError("Input tensors must be of type tf.Tensor")
    if y_test.shape != y_pred_argmax.shape:
        raise ValueError("Input tensors must have the same shape")
    # if len(y_test.shape) != 1:
    #     raise ValueError("Input tensors must be 1D")

# Convert to appropriate tensor format if not already
y_test_tensor = tf.convert_to_tensor(y_test_)
y_pred_argmax_tensor = tf.convert_to_tensor(y_pred_argmax_)

# Remove the extra dimension from y_test if needed
y_test_tensor = tf.squeeze(y_test_tensor)

# Validate input
validate_input(y_test_tensor, y_pred_argmax_tensor)

# Pixel Accuracy
accuracy = tf.keras.metrics.Accuracy()
accuracy.update_state(y_test_tensor, y_pred_argmax_tensor)
pixel_accuracy = accuracy.result().numpy()

# Mean IoU and Confusion Matrix
miou = tf.keras.metrics.MeanIoU(num_classes=n_classes)
miou.update_state(y_test_tensor, y_pred_argmax_tensor)
mean_iou = miou.result().numpy()
confusion_matrix = miou.total_cm

# Function to calculate metrics
def calculate_metric(y_true, y_pred, class_index, metric):
    y_true_class = tf.cast(tf.equal(y_true, class_index), tf.float32)
    y_pred_class = tf.cast(tf.equal(y_pred, class_index), tf.float32)
    intersection = tf.reduce_sum(y_true_class * y_pred_class)
    union = tf.reduce_sum(y_true_class) + tf.reduce_sum(y_pred_class) - intersection
    
    if metric == 'iou':
        # Handle edge case where union is zero
        return tf.cond(tf.equal(union, 0), lambda: 0.0, lambda: intersection / union)
    elif metric == 'dice':
        # Handle edge case where sum of true and predicted is zero
        return tf.cond(tf.equal(tf.reduce_sum(y_true_class) + tf.reduce_sum(y_pred_class), 0), lambda: 0.0, lambda: (2. * intersection) / (tf.reduce_sum(y_true_class) + tf.reduce_sum(y_pred_class)))
    elif metric == 'precision':
        # Handle edge case where predicted is zero
        return tf.cond(tf.equal(tf.reduce_sum(y_pred_class), 0), lambda: 0.0, lambda: intersection / tf.reduce_sum(y_pred_class))
    elif metric == 'recall':
        # Handle edge case where true is zero
        return tf.cond(tf.equal(tf.reduce_sum(y_true_class), 0), lambda: 0.0, lambda: intersection / tf.reduce_sum(y_true_class))
    else:
        raise ValueError("Invalid metric. Choose from 'iou', 'dice', 'precision', 'recall'.")

# Calculate per-class metrics
per_class_metrics = []
for i in range(n_classes):
    iou = calculate_metric(y_test_tensor, y_pred_argmax_tensor, i, 'iou')
    dice = calculate_metric(y_test_tensor, y_pred_argmax_tensor, i, 'dice')
    precision = calculate_metric(y_test_tensor, y_pred_argmax_tensor, i, 'precision')
    recall = calculate_metric(y_test_tensor, y_pred_argmax_tensor, i, 'recall')
    per_class_metrics.append((iou.numpy(), dice.numpy(), precision.numpy(), recall.numpy()))

# Cohen's Kappa
n = tf.cast(tf.reduce_sum(confusion_matrix), tf.float32)
sum_po = tf.cast(tf.linalg.trace(confusion_matrix), tf.float32)
sum_pe = tf.reduce_sum(tf.cast(tf.reduce_sum(confusion_matrix, axis=0) * tf.reduce_sum(confusion_matrix, axis=1), tf.float32)) / n
po = sum_po / n
pe = sum_pe / n
kappa = (po - pe) / (1 - pe + tf.keras.backend.epsilon())

# Print results
print(f"Pixel Accuracy: {pixel_accuracy}")
print(f"Mean IoU: {mean_iou}")

print("IoU:")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[0]}")

print("Precision:")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[2]}")

print("Recall:")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[3]}")

print("F1 Score (Dice Coefficient):")
for i, metrics in enumerate(per_class_metrics):
    print(f"  Class {i}: {metrics[1]}")

print(f"Mean Dice Coefficient (F1 Score): {np.mean([m[1] for m in per_class_metrics])}")
print(f"Cohen's Kappa: {kappa.numpy()}")

##### Visualizations
import seaborn as sns

# Plot confusion matrix
conf_matrix = confusion_matrix.numpy()
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# Extract IoU and Dice Coefficient for each class
class_indices = list(range(n_classes))
iou_values = [m[0] for m in per_class_metrics]
dice_values = [m[1] for m in per_class_metrics]

# Plot IoU
plt.figure(figsize=(10, 5))
plt.bar(class_indices, iou_values, color='skyblue')
plt.xlabel('Class Index')
plt.ylabel('IoU')
plt.title('Class-wise IoU')
plt.show()

# Plot Dice Coefficient
plt.figure(figsize=(10, 5))
plt.bar(class_indices, dice_values, color='lightgreen')
plt.xlabel('Class Index')
plt.ylabel('Dice Coefficient')
plt.title('Class-wise Dice Coefficient')
plt.show()

# Function to plot individual sample predictions
def plot_individual_sample_prediction(image, true_mask, pred_mask, index):
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.title('Testing Image')
    plt.imshow(image[:,:,0], cmap='gray')
    
    plt.subplot(1, 3, 2)
    plt.title('Testing Label')
    plt.imshow(true_mask[:,:,0], cmap='jet')
    
    plt.subplot(1, 3, 3)
    plt.title('Prediction on test image')
    plt.imshow(pred_mask, cmap='jet')
    
    plt.suptitle(f'Sample {index}')
    plt.show()

# Generating a few sample predictions
n_samples = 50  # Number of samples to display
sample_indices = random.sample(range(len(X_test1)), n_samples)

for idx, sample_idx in enumerate(sample_indices):
    test_img = X_test1[sample_idx]
    ground_truth = y_test[sample_idx]
    
    test_img_input = np.expand_dims(test_img, 0)
    prediction = model.predict(test_img_input)
    predicted_img = np.argmax(prediction, axis=3)[0,:,:]
    
    # Plotting the individual sample prediction
    plot_individual_sample_prediction(test_img, ground_truth, predicted_img, idx + 1)


###
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import tensorflow as tf

# Assuming y_test and model1 are available
# Convert y_test to one-hot encoding
n_classes = 3  # Number of classes
y_test_onehot = tf.keras.utils.to_categorical(y_test, num_classes=n_classes)

# Get the predicted probabilities from the model
y_pred_probs = model.predict(X_test1)  # Predicted probabilities

# Flatten the arrays for ROC calculation
y_test_onehot_flat = y_test_onehot.reshape(-1, n_classes)
y_pred_probs_flat = y_pred_probs.reshape(-1, n_classes)

# Calculate ROC curve and AUC for each class
fpr = {}
tpr = {}
roc_auc = {}

for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test_onehot_flat[:, i], y_pred_probs_flat[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
    print(f"Class {i} - FPR: {fpr[i]}")
    print(f"Class {i} - TPR: {tpr[i]}")
    print(f"Class {i} - AUC: {roc_auc[i]:.2f}\n")

# Plotting the ROC curves
plt.figure(figsize=(10, 8))
for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label=f'Class {i} (area = {roc_auc[i]:.2f})')
    
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc='lower right')
plt.show()
```