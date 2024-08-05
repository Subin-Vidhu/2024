
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

# Ensure predicted_class_indices has the same shape as ground_truth_labels
if len(predicted_class_indices_tensor.shape) < len(ground_truth_labels_tensor.shape):
    predicted_class_indices_tensor = tf.expand_dims(predicted_class_indices_tensor, axis=-1) # Add channel dimension if missing
```

## Pixel Accuracy
**Definition**: Pixel accuracy is the proportion of correctly classified pixels to the total number of pixels.

**Formula**: 
\[
\text{Pixel Accuracy} = \frac{\sum_{i=1}^{n} \mathbf{1}(y_i = \hat{y}_i)}{n}
\]

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
\[
\text{IoU} = \frac{|A \cap B|}{|A \cup B|}
\]

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
\[
\text{IoU} = \frac{|A \cap B|}{|A \cup B|}
\]

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
\[
\text{Dice Coefficient} = \frac{2 \cdot |A \cap B|}{|A| + |B|}
\]

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
\[
\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}
\]

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
\[
\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}
\]

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
\[
\kappa = \frac{p_o - p_e}{1 - p_e}
\]
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


### Full Code
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