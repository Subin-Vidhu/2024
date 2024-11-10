# Print the first 5 rows of the DataFrame
print(heart_disease_df.head())

# Print information about the DataFrame
print(heart_disease_df.info())

# Visualize the cholesterol column
heart_disease_df['chol'].plot(kind='hist')

# Set the title and axis labels
plt.title('Cholesterol distribution')
plt.xlabel('Cholesterol')
plt.ylabel('Frequency')
plt.show()

"""Finding class imbalance
You are focusing on the important preliminary phase of the machine learning lifecycle: Exploratory Data Analysis (EDA).

EDA allows you to better understand the nature of the heart_disease_df dataset, including the relationships between different variables, and potential problems that might need to be addressed before you move on to training your model. Understanding the distribution of classes in your features - for example, patient sex - is a key part of EDA.

Class imbalance, where one class has significantly more samples than another, can potentially bias your model's training process, leading it to favor the majority class."""

# Print the sex value counts of the heart disease dataset
print(heart_disease_df['sex'].value_counts())

# Drop empty columns
heart_disease_column_dropped = heart_disease_df.drop(['oldpeak'], axis=1)

# Drop duplicate rows
heart_disease_duplicates_dropped = heart_disease_column_dropped.drop_duplicates()

# Calculate the mean value of the restecg column
mean_value = heart_disease_duplicates_dropped['restecg'].mean()

# Impute missing values with the mean
heart_disease_duplicates_dropped['restecg'].fillna(mean_value, inplace=True)
print(heart_disease_duplicates_dropped['restecg'].isna().any())

"""Normalization and Standardization
Feature scaling helps ensure that no feature dominates others during modeling. Normalization and Standardization are widely used feature scaling techniques. Normalization typically scales features in the range [0, 1] ensuring they have roughly the same scale. Standardization transforms the data to have zero mean and unit variance, maintaining more information about outliers and not bounding the range. matplotlib.pyplot has been imported as plt, MinMaxScaler and StandardScaler have been imported, and the split heart disease data features have been imported as X_train and X_test."""

# Standardize 'age' on the training set and use the same standardizer to transform the 'age' column of the test set to avoid data leakage
standardizer = StandardScaler()
X_train['age'] = standardizer.fit_transform(X_train['age'].values.reshape(-1,1))
X_test['age'] = standardizer.transform(X_test['age'].values.reshape(-1,1))

plt.figure(figsize=(10,5))
plt.hist(X_train['age'], bins=30, alpha=0.5, label='Standardized')
plt.legend(prop={'size': 16})
plt.title('Histogram with Standardized Age')
plt.xlabel('Standardized Age')
plt.ylabel('Count')
plt.show()

"""Feature selection
While preparing your data for modeling, it is important to ensure that you have a set of helpful features for the model to base its predictions (or diagnosis) on. In order to be helpful, features need to capture essential characteristics of the heart disease dataset in an orthogonal way; more data isn't always better!

You can use the sklearn.feature_selection.SelectFromModel module to select useful features. SelectFromModel implements a brute-force method that uses a RandomForestClassifier model to find the most salient features for the task of heart disease diagnosis.

RandomForestClassifier has been imported and the heart disease data features and target have been imported as X_train and y_train, respectively."""

from sklearn.feature_selection import SelectFromModel

# Define the random forest model and fit to the training data
rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
rf.fit(X_train, y_train)

# Define the feature selection object
model = SelectFromModel(rf, prefit=True)

# Transform the training features
X_train_transformed = model.transform(X_train)

original_features = heart_disease_df.columns[:-1]
print(f"Original features: {original_features}")

# Select the features deemed important by the SelectFromModel
features_bool = model.get_support()

selected_features = original_features[features_bool]
print(f"\nSelected features: {selected_features}")

feature_importance = pd.DataFrame({
    "feature": selected_features,
    "importance": rf.feature_importances_[features_bool]
})
plt.figure(figsize=(10, 6))
plt.barh(feature_importance["feature"], feature_importance["importance"])
plt.show()

"""Training a model
In the video, you learned how to train a model using scikit learn. In this exercise, you will demonstrate your new skills by training a support vector classifier (SVC) model on the heart disease dataset. Your job is to split the data into training and testing portions, define the necessary model with the correct parameters, and train it on the split data. The heart disease data features and target have been imported as heart_disease_X and heart_disease_y, respectively"""

# Import required modules
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Split the data into training and testing sets (80:20)
X_train, X_test, y_train, y_test = train_test_split(heart_disease_X, heart_disease_y, test_size=0.2, random_state=42)

# Define the SVM / SVC model
svc_model = SVC(kernel='linear')
svc_model.fit(X_train, y_train)

# Get predictions from the model
y_pred = svc_model.predict(X_test)
print(y_pred)
"""
MLFlow for logging and retrieving data
MLflow is an open-source platform for managing the ML lifecycle. It can be used to keep track of experiments, packaging code into reproducible runs, and sharing and deploying models. In the following exercise, you will log some of the parameters of a training experiment for your heart disease model. mlflow is imported, and the trained heart disease model has been loaded for you."""

# Initialize the MLflow experiment
mlflow.set_experiment("Logistic Regression Heart Disease Prediction")

# Start a run, log model coefficients and intercept
with mlflow.start_run():
    for idx, coef in enumerate(model.coef_[0]):
        mlflow.log_param(f"coef_{idx}", coef)
    mlflow.log_param("intercept", model.intercept_[0])

    run_id = mlflow.active_run().info.run_id
    print(run_id)

"""KFold cross validation
When working with ML models, it's essential to evaluate their performance on unseen data while ensuring that. One common technique for this purpose is k-fold cross-validation. In this exercise, you'll explore how the k-fold cross-validation technique splits a dataset into training and testing sets. KFold is imported for you, as well as the heart disease dataset features heart_disease_df_X."""    


# Create a KFold object
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

# Get the train and test data from the first split from the shuffled KFold
train_data_split, test_data_split = next(kfold.split(heart_disease_df_X))

# Print out the number of datapoints in the original training set, as well as the train and test splits
print("Number of training datapoints in heart_disease_df_X:", len(heart_disease_df_X))
print("Number of training datapoints in split:", len(train_data_split))
print("Number of testing datapoints in split:", len(test_data_split))

"""Evaluating a model
Throughout this course, you've been working on a project to classify heart disease using machine learning. You've successfully cleaned the dataset, performed feature engineering, and trained your model.

Here, you will employ the methods you have learned so far for model evaluation. You will evaluate a machine learning model using appropriate error metrics, visualize the evaluation results, and identify potential overfitting in preparation for deployment. By the end of this exercise, you will have gained a deeper understanding of model evaluation and visualization techniques.

The trained logistic regression model is loaded as model
KFold and cross_val_score are imported from sklearn.model_selection
confusion_matrix is imported from sklearn.metrics.
The variables heart_disease_df_X and heart_disease_df_y have been already imported."""

# Evaluate model using k-fold cross-validation
kf = KFold(n_splits=5)

# Compute the cross-validation score
score = cross_val_score(model, heart_disease_df_X, heart_disease_df_y, scoring='balanced_accuracy', cv=kf)
print(score)

# Get model predictions
y_pred = model.predict(heart_disease_df_X)

# Print confusion matrix
cm = confusion_matrix(heart_disease_df_y, y_pred)
print(cm)

