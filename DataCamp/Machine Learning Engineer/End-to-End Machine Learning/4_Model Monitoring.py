"""Visualizing a deployed model's output over time
In this exercise, you will utilize data from two separate months - January and February - to monitor changes in your heart disease model's predictions over time. As you know, your model has been trained to perform a binary classification task of heart disease classification, and you have recorded the model's predictions in the logs for these two months.

Assume that the logs of the model's predictions over the last two months have been generated through Elastic Beanstalk and have been imported as pandas DataFrame, called logs_january and logs_february, with a target column of the predictions for that month. matplotlib.pyplot has been imported as plt."""

fig, ax = plt.subplots(1, 2, figsize=(15, 6))  # 1 row, 2 columns
# January Plot
logs_january['target'].value_counts().plot(kind='bar', ax=ax[0])
ax[0].set_title('Distribution of Predicted Classes - January')
ax[0].set_xlabel('Class')
ax[0].set_ylabel('Frequency')

# February Plot
logs_february['target'].value_counts().plot(kind='bar', ax=ax[1])
ax[1].set_title('Distribution of Predicted Classes - February')
ax[1].set_xlabel('Class')
ax[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

"""Detecting data drift using the Kolmogorov-Smirnov test
After successfully deploying your heart disease prediction model, you've been monitoring its performance and input data. You've noticed that the distribution of some key features in the recent data collected in February looks a bit different from the data you trained on in January. Such discrepancies can affect the model's performance, and it's crucial to detect and address them.

In this exercise, you will use the Kolmogorov-Smirnov (K-S) test to detect any potential data drift between the January and February datasets. Sample datasets called january_data and february_data are already loaded for you."""

# Import the ks_2samp function
from scipy.stats import ks_2samp

# Calculate the test statistic and p value
test_statistic, p_value = ks_2samp(january_data, february_data)

# Check the p-value and print the detection result
if p_value < 0.05:
    print("Data drift detected.")
else:
    print("No data drift detected.")

"""Feedback loops
In real-world ML applications, it's not enough to just deploy a model and forget about it. As the data evolves, so should the model. The feedback loop is a way of ensuring that the model is continuously learning and adapting to changing data. Imagine that your heart disease model has been in production for a few months. As part of continuous monitoring and improvement, you want to assess the model's current performance and determine the need for potential retraining or adjustments. balanced_accuracy_score is imported for you from sklearn.metrics, ks_2samp is imported from scipy.stats, and two samples of the models true_labels_feb and predicted_labels_feb for the current time period have been predefined. Finally jan_data_samples and feb_data_samples have been loaded."""    

# Calculate and print the balanced accuracy of the model
balanced_accuracy_jan = 60.0
balanced_accuracy_feb = balanced_accuracy_score(true_labels_feb, predicted_labels_feb) * 100
print(f"Model Balanced Accuracy In February: {balanced_accuracy_feb:.2f}%")
print(f"Is there a decline in accuracy? {'Yes' if balanced_accuracy_feb < balanced_accuracy_jan else 'No'}")

# Use the Kolmogorov-Smirnov test to check for data drift
ks_statistic, p_value = ks_2samp(jan_data_samples, feb_data_samples)

significant_drift = p_value < 0.05

print(f"Kolmogorov-Smirnov Statistic: {ks_statistic:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Is there significant data drift? {'Yes' if significant_drift else 'No'}")

