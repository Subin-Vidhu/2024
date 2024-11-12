"""Load the dataset
NannyML comes with a set of internal datasets in order to make it easier to demo use cases and test different algorithms. To load the dataset, you only need to use the nannyml.load_us_census_ma_employment_data() function.

The function returns three Pandas DataFrame objects: the reference set (the test set), the analysis set (unseen production data), and the ground truth for the analysis set. These data frames should be named according to the convention as reference, analysis, and analysis_gt.

In this exercise, you will load the US Census Employment dataset and print the data frames to understand what they look like."""

# Import nannyml
import nannyml

# Load the US Census Employment dataset
reference, analysis, analysis_gt = nannyml.load_us_census_ma_employment_data()

# Print head of the reference data
print(reference.head())

# Print head of the analysis data
print(analysis.head())

"""Loading and splitting the data
To deploy and monitor a model in production, you must first create it. In the last video, you've been introduced to loading and processing data, building the model, and creating reference and analysis sets.

In this exercise, you'll follow a similar process, but to simplify matters, you'll use the NYC Green Taxi dataset provided in a csv file that's already been processed.

For this exercise, pandas has been imported as pd and is ready for you to use."""

# Load the dataset
dataset_name = "green_taxi_dataset.csv"
data = pd.read_csv(dataset_name)
features = ['lpep_pickup_datetime', 'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount', 'pickup_time']
target = 'tip_amount'

# Split the training data
X_train = data.loc[data['partition'] == 'train', features]
y_train = data.loc[data['partition'] == 'train', target]

# Split the test data
X_test = data.loc[data['partition'] == 'test', features]
y_test = data.loc[data['partition'] == 'test', target]

# Split the prod data
X_prod = data.loc[data['partition'] == 'prod', features]
y_prod = data.loc[data['partition'] == 'prod', target]

"""Creating reference and analysis set
After your data is split into train, test, and production sets, you can build and deploy your model. The testing and production data will later be used to create the reference and analysis set.

In this exercise, you will go through this process. You have all of your X_train/test/prod, and y_train/test/prod datasets created in the previous exercise already loaded here.

For this exercise, pandas has been imported as pd and is ready for use."""

from lightgbm import LGBMRegressor

# Fit the model
model = LGBMRegressor(random_state=111, n_estimators=50, n_jobs=1)
model.fit(X_train, y_train)

# Get model's prediction on train, test, and production set
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)
y_pred_prod = model.predict(X_prod)

# Create reference and analysis set
reference = X_test.copy() # Copy test set features
reference['y_pred'] = y_pred_test # Add models predictions on test set
reference['tip_amount'] = y_test # Add labels(ground truth)
reference = reference.join(data['lpep_pickup_datetime']) # Add timestamp column

analysis = X_prod.copy() # Copy production set features
analysis['y_pred'] = y_pred_prod # Add models predictions on production set
analysis = analysis.join(data['lpep_pickup_datetime']) # Add timestamp column

"""Performance estimation for tip prediction
In the previous exercises, you prepared a reference and analysis set for the NYC Green Taxi dataset. In this one, you will use that data to estimate the model's performance in production.

First, you must initialize the DLE algorithm with the provided parameters and then plot the results.

The reference and analysis set is already loaded and saved in the reference and analysis variables. Additionally, nannyml is also already imported."""

estimator = nannyml.DLE(y_pred='y_pred',
    timestamp_column_name='lpep_pickup_datetime',
    feature_column_names=features,
    chunk_period='d',
    y_true='tip_amount',
    metrics=['mse'])

# Fit the reference data to the DLE algorithm
estimator.fit(reference)

# Estimate the performance on the analysis data
results = estimator.estimate(analysis)

# Plot and show the results
results.plot().show()
