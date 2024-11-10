"""Writing unit tests
In the previous video on inference testing, you learned about the importance of writing test cases for your trained and evaluated model using the Python unittest library. In this exercise, you will put your new skills to the test by writing a test case for the model to check that it is producing binary outputs as expected. Your trained model is imported, as well as the testing portion of the dataset X_test."""

import unittest
import numpy as np

# Create a class called TestModelInference
class TestModelInference(unittest.TestCase):
	def setUp(self):
		self.model = model

		# set X_test as a class attribute
		self.X_test = X_test

	# define a test for prediction output values
	def test_prediction_output_values(self):
		print("Running test_prediction_output_values test case")

		# Get model predictions
		y_pred = self.model.predict(self.X_test)
		unique_values = np.unique(y_pred)
		for value in unique_values:
			self.assertIn(value, [0, 1])

"""Defining features for a feature store
Before creating a feature store, you need to ensure that features are formally defined, in order to ensure the feature store knows the relationships, type, and structure of the features to be loaded. In this exercise, you will formally define a number of features in preparation for the creation of a feature store. Field is imported for you from feast."""            

# Define entity and selected features
patient = Entity(name="patient", join_keys=["patient_id"])
cp = Field(name="cp", dtype=Float32)
thalach = Field(name="thalach", dtype=Int32)
ca = Field(name="ca", dtype=Int32)
thal = Field(name="thal", dtype=Int32)

"""Feature store using Feast
In order to ensure effective development throughout the machine learning lifecycle, it is important to maintain detailed and comprehensive records of resources. Feature stores and model registries are examples of helpful resource records in the pre-modelling and modelling phases. In this exercise, you will implement a feature store using Feast. The predefined patient, Entity, as well as the cp, thalach, ca, and thal features have been loaded for you. ValueType, FeatureStore, and FileSource are all imported from feast. heart_disease_df is also imported."""

heart_disease_df.to_parquet("heart_disease.parquet")

# Point File Source to the saved file
data_source = FileSource(
    path="heart_disease.parquet",
    event_timestamp_column="timestamp",
    created_timestamp_column="created",
)

# Create a Feature View of the features
heart_disease_fv = FeatureView(
    name="heart_disease",
    entities=[patient],
    schema=[cp, thalach, ca, thal],
    source=data_source,
)

# Create a store of the data and apply the features
store = FeatureStore(repo_path=".")
store.apply([patient, heart_disease_fv])

