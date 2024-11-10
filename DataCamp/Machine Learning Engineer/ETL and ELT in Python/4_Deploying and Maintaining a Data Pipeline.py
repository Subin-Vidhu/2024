"""Validating a data pipeline at "checkpoints"
In this exercise, you'll be working with a data pipeline that extracts tax data from a CSV file, creates a new column, filters out rows based on average taxable income, and persists the data to a parquet file.

pandas has been loaded as pd, and the extract(), transform(), and load() functions have already been defined. You'll use these functions to validate the data pipeline at various checkpoints throughout its execution."""

# Extract and transform tax_data
raw_tax_data = extract("raw_tax_data.csv")
clean_tax_data = transform(raw_tax_data)

# Check the shape of the raw_tax_data DataFrame, compare to the clean_tax_data DataFrame
print(f"Shape of raw_tax_data: {raw_tax_data.shape}")
print(f"Shape of clean_tax_data: {clean_tax_data.shape}")

"""Validating a data pipeline at "checkpoints"
In this exercise, you'll be working with a data pipeline that extracts tax data from a CSV file, creates a new column, filters out rows based on average taxable income, and persists the data to a parquet file.

pandas has been loaded as pd, and the extract(), transform(), and load() functions have already been defined. You'll use these functions to validate the data pipeline at various checkpoints throughout its execution."""

raw_tax_data = extract("raw_tax_data.csv")
clean_tax_data = transform(raw_tax_data)
load(clean_tax_data, "clean_tax_data.parquet")

print(f"Shape of raw_tax_data: {raw_tax_data.shape}")
print(f"Shape of clean_tax_data: {clean_tax_data.shape}")

to_validate = pd.read_parquet("clean_tax_data.parquet")
print(clean_tax_data.head(3))
print(to_validate.head(3))

# Check that the DataFrames are equal
print(to_validate.equals(clean_tax_data))

"""Testing a data pipeline end-to-end
In this exercise, you'll be working with the same data pipeline as before, which extracts, transforms, and loads tax data. You'll practice testing this pipeline end-to-end to ensure the solution can be run multiple times, without duplicating the transformed data in the parquet file.

pandas has been loaded as pd, and the extract(), transform(), and load() functions have already been defined."""

# Trigger the data pipeline to run three times
for attempt in range(0, 3):
	print(f"Attempt: {attempt}")
	raw_tax_data = extract("raw_tax_data.csv")
	clean_tax_data = transform(raw_tax_data)
	load(clean_tax_data, "clean_tax_data.parquet")
	
	# Print the shape of the cleaned_tax_data DataFrame
	print(f"Shape of clean_tax_data: {clean_tax_data.shape}")
    
# Read in the loaded data, check the shape
to_validate = pd.read_parquet("clean_tax_data.parquet")
print(f"Final shape of cleaned data: {to_validate.shape}")


"""Validating a data pipeline with assert
To build unit tests for data pipelines, it's important to get familiar with the assert keyword, and the isinstance() function. In this exercise, you'll practice using these two tools to validate components of a data pipeline.

The functions extract() and transform() have been made available for you, along with pandas, which has been imported as pd. Both extract() and transform() return a DataFrame"""

raw_tax_data = extract("raw_tax_data.csv")
clean_tax_data = transform(raw_tax_data)

# Assert that clean_tax_data takes is an instance of a string
try:
	assert isinstance(clean_tax_data, str)
except Exception as e:
	print(e)

"""Writing unit tests with pytest
In this exercise, you'll practice writing a unit test to validate a data pipeline. You'll use assert and other tools to build the tests, and determine if the data pipeline performs as it should.

The functions extract() and transform() have been made available for you, along with pandas, which has been imported as pd. You'll be testing the transform() function, which is shown below.

def transform(raw_data):
    raw_data["average_taxable_income"] = raw_data["total_taxable_income"] / raw_data["number_of_firms"]
    clean_data = raw_data.loc[raw_data["average_taxable_income"] > 100, :]
    clean_data.set_index("industry_name", inplace=True)
    return clean_data"""

import pytest

def test_transformed_data():
    raw_tax_data = extract("raw_tax_data.csv")
    clean_tax_data = transform(raw_tax_data)
    
    # Assert that the transform function returns a pd.DataFrame
    assert isinstance(clean_tax_data, pd.DataFrame)
    
    # Assert that the clean_tax_data DataFrame has more columns than the raw_tax_data DataFrame
    assert len(clean_tax_data.columns) > len(raw_tax_data.columns)

"""Creating fixtures with pytest
When building unit tests, you'll sometimes have to do a bit of setup before testing can begin. Doing this setup within a unit test can make the tests more difficult to read, and may have to be repeated several times. Luckily, pytest offers a way to solve these problems, with fixtures.

For this exercise, pandas has been imported as pd, and the extract() function shown below is available for use!

def extract(file_path):
    return pd.read_csv(file_path)"""

# Import pytest
import pytest

# Create a pytest fixture
@pytest.fixture()
def raw_tax_data():
	raw_data = extract("raw_tax_data.csv")
   
    # Return the raw DataFrame
	return raw_data

"""Unit testing a data pipeline with fixtures
You've learned in the last video that unit testing can help to instill more trust in your data pipeline, and can even help to catch bugs throughout development. In this exercise, you'll practice writing both fixtures and unit tests, using the pytest library and assert.

The transform function that you'll be building unit tests around is shown below for reference. pandas has been imported as pd, and the pytest() library is loaded and ready for use.

def transform(raw_data):
    raw_data["tax_rate"] = raw_data["total_taxes_paid"] / raw_data["total_taxable_income"]
    raw_data.set_index("industry_name", inplace=True)
    return raw_data"""

# Define a pytest fixture
@pytest.fixture()
def clean_tax_data():
    raw_data = pd.read_csv("raw_tax_data.csv")
    
    # Transform the raw_data, store in clean_data DataFrame, and return the variable
    clean_data = transform(raw_data)
    return clean_data    

@pytest.fixture()
def clean_tax_data():
    raw_data = pd.read_csv("raw_tax_data.csv")
    clean_data = transform(raw_data)
    return clean_data

# Pass the fixture to the function
def test_tax_rate(clean_tax_data):
    # Assert values are within the expected range
    assert clean_tax_data["tax_rate"].max() <= 1 and clean_tax_data["tax_rate"].min() >= 0

"""Data pipeline architecture patterns
When building data pipelines, it's best to separate the files where functions are being defined from where they are being run.

In this exercise, you'll practice importing components of a pipeline into memory before using these functions to run the pipeline end-to-end. The project takes the following format, where pipeline_utils stores the extract(), transform(), and load() functions that will be used run the pipeline.

> ls
 etl_pipeline.py
 pipeline_utils.py"""

 # Import the extract, transform, and load functions from pipeline_utils
from pipeline_utils import extract, transform, load

# Run the pipeline end to end by extracting, transforming and loading the data
raw_tax_data = extract("raw_tax_data.csv")
clean_tax_data = transform(raw_tax_data)
load(clean_tax_data, "clean_tax_data.parquet")

"""Running a data pipeline end-to-end
It's important to monitor the performance of a pipeline when running in production. Earlier in the course, you explored tools such as exception handling and logging. In this last exercise, we'll practice running a pipeline end-to-end, while monitoring for exceptions and logging performance."""

import logging
from pipeline_utils import extract, transform, load

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

try:
	raw_tax_data = extract("raw_tax_data.csv")
	clean_tax_data = transform(raw_tax_data)
	load(clean_tax_data, "clean_tax_data.parquet")
    
	logging.info("Successfully extracted, transformed and loaded data.")  # Log a success message.
    
except Exception as e:
	logging.error(f"Pipeline failed with error: {e}")  # Log failure message

