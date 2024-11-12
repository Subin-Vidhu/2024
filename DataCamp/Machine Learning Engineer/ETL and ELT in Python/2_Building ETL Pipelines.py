"""Extracting data from parquet files
One of the most common ways to ingest data from a source system is by reading data from a file, such as a CSV file. As data has gotten bigger, the need for better file formats has brought about new column-oriented file types, such as parquet files.

In this exercise, you'll practice extracting data from a parquet file."""

import pandas as pd

# Read the sales data into a DataFrame
sales_data = pd.read_parquet("sales_data.parquet", engine="fastparquet")

# Check the data type of the columns of the DataFrames
print(sales_data.dtypes)

# Print the shape of the DataFrame, as well as the head
print(sales_data.shape)
print(sales_data.head())

"""Pulling data from SQL databases
SQL databases are one of the most used data storage tools in the world. Many companies have teams of several individuals responsible for creating and maintaining these databases, which typically store data crucial for day-to-day operations. These SQL databases are commonly used as source systems for a wide range of data pipelines.

For this exercise, pandas has been imported as pd. Best of luck!"""

import sqlalchemy

# Create a connection to the sales database
db_engine = sqlalchemy.create_engine("postgresql+psycopg2://repl:password@localhost:5432/sales")

# Query all rows and columns of the sales table
raw_sales_data = pd.read_sql("SELECT * FROM sales", db_engine)
print(raw_sales_data)


"""Building functions to extract data
It's important to modularize code when building a data pipeline. This helps to make pipelines more readable and reusable, and can help to expedite troubleshooting efforts. Creating and using functions for distinct operations in a pipeline can even help when getting started on a new project by providing a framework to begin development.

pandas has been imported as pd, and sqlalchemy is ready to be used."""

def extract():
    connection_uri = "postgresql+psycopg2://repl:password@localhost:5432/sales"
    db_engine = sqlalchemy.create_engine(connection_uri)
    raw_data = pd.read_sql("SELECT * FROM sales WHERE quantity_ordered = 1", db_engine)
    
    # Print the head of the DataFrame
    print(raw_data.head())
    
    # Return the extracted DataFrame
    return raw_data
    
# Call the extract() function
raw_sales_data = extract()


"""Filtering pandas DataFrames
Once data has been extracted from a source system, it's time to transform it! Often, source data may have more information than what is needed for downstream use cases. If this is the case, dimensionality should be reduced during the "transform" phase of the data pipeline.

pandas has been imported as pd, and the extract() function is available to load a DataFrame from the path that is passed."""

# Extract data from the sales_data.parquet path
raw_sales_data = extract("sales_data.parquet")

def transform(raw_data):
  	# Only keep rows with `Quantity Ordered` greater than 1
    clean_data = raw_data.loc[raw_data["Quantity Ordered"] > 1, :]
	
    # Only keep columns "Order Date", "Quantity Ordered", and "Purchase Address"
    clean_data = clean_data.loc[:, ["Order Date", "Quantity Ordered", "Purchase Address"]]
	
    # Return the filtered DataFrame
    return clean_data
    
transform(raw_sales_data)


"""Transforming sales data with pandas
Before insights can be extracted from a dataset, column types may need to be altered to properly leverage the data. This is especially common with temporal data types, which can be stored in several different ways.

For this example, pandas has been import as pd and is ready for you to use."""

raw_sales_data = extract("sales_data.csv")

def transform(raw_data):
    # Convert the "Order Date" column to type datetime
    raw_data["Order Date"] = pd.to_datetime(raw_data["Order Date"], format="%m/%d/%y %H:%M")
    
    # Only keep items under ten dollars
    clean_data = raw_data.loc[raw_data["Price Each"] < 10, :]
    return clean_data

clean_sales_data = transform(raw_sales_data)

# Check the data types of each column
print(clean_sales_data.dtypes)


"""Validating data transformations
Great work so far! Manually spot-checking transformations is a great first step to ensuring that you're maintaining data quality throughout a pipeline. pandas offers several built-in functions to help you with just that!

To help get you started with this exercise, pandas has been imported as pd."""

def extract(file_path):
    raw_data = pd.read_parquet(file_path)
    return raw_data

raw_sales_data = extract("sales_data.parquet")

def transform(raw_data):
  	# Filter rows and columns
    clean_data = raw_data.loc[raw_data["Quantity Ordered"] == 1, ["Order ID", "Price Each", "Quantity Ordered"]]
    return clean_data

# Transform the raw_sales_data
clean_sales_data = transform(raw_sales_data)

"""Loading sales data to a CSV file
Loading data is an essential component of any data pipeline. It ensures that any data consumers and processes have reliable access to data that you've extracted and transformed earlier in a pipeline. In this exercise, you'll practice loading transformed sales data to a CSV file using pandas, which has been imported as pd. In addition to this, the raw data has been extracted and is available in the DataFrame raw_sales_data."""

def transform(raw_data):
	# Find the items prices less than 25 dollars
	return raw_data.loc[raw_data["Price Each"] < 25, ["Order ID", "Product", "Price Each", "Order Date"]]

def load(clean_data):
	# Write the data to a CSV file without the index column
	clean_data.to_csv("transformed_sales_data.csv", index=False)


clean_sales_data = transform(raw_sales_data)

# Call the load function on the cleaned DataFrame
load(clean_sales_data)

"""Customizing a CSV file
Sometimes, data needs to be stored in a CSV file in a customized manner. This may include using different header values, including or excluding the index column of a DataFrame, or altering the character used to separate columns. In this example, you'll get to practice this, as well as ensuring that the file is stored in the desired file path.

The pandas library has been imported as pd, and the data has already been transformed to include only rows with a "Quantity Ordered" greater than one. The cleaned DataFrame is stored in a variable named clean_sales_data."""

# Import the os library
import os

# Load the data to a csv file with the index, no header and pipe separated
def load(clean_data, path_to_write):
	clean_data.to_csv(path_to_write, header=False, sep="|")

load(clean_sales_data, "clean_sales_data.csv")

# Check that the file is present.
file_exists = os.path.exists("clean_sales_data.csv")
print(file_exists)

"""Persisting data to files
Loading data to a final destination is one of the most important steps of a data pipeline. In this exercise, you'll use the transform() function shown below to transform product sales data before loading it to a .csv file. This will give downstream data consumers a better view into total sales across a range of products.

For this exercise, the sales data has been loaded and transformed, and is stored in the clean_sales_data DataFrame. The pandas package has been imported as pd, and the os library is also ready to use!"""

def load(clean_data, file_path):
    # Write the data to a file
    clean_data.to_csv(file_path, header=False, index=False)

    # Check to make sure the file exists
    file_exists = os.path.exists(file_path)
    if not file_exists:
        raise Exception(f"File does NOT exists at path {file_path}")

# Load the transformed data to the provided file path
load(clean_sales_data, "transformed_sales_data.csv")

"""Logging within a data pipeline
In this exercise, we'll take a look back at the function you wrote in a previous video and practice adding logging to the function. This will help when troubleshooting errors or making changes to the logic!

pandas has been imported as pd. In addition to this, the logging module has been imported, and the default log-level has been set to "debug"."""

def transform(raw_data):
    raw_data["Order Date"] = pd.to_datetime(raw_data["Order Date"], format="%m/%d/%y %H:%M")
    clean_data = raw_data.loc[raw_data["Price Each"] < 10, :]
    
    # Create an info log regarding transformation
    logging.info("Transformed 'Order Date' column to type 'datetime'.")
    
    # Create debug-level logs for the DataFrame before and after filtering
    logging.debug(f"Shape of the DataFrame before filtering: {raw_data.shape}")
    logging.debug(f"Shape of the DataFrame after filtering: {clean_data.shape}")
    
    return clean_data
  
clean_sales_data = transform(raw_sales_data)

"""Handling exceptions when loading data
Sometimes, your data pipelines might throw an exception. These exceptions are a form of alerting, and they let a Data Engineer know when something unexpected happened. It's important to properly handle these exceptions. In this exercise, we'll practice just that!

To help get you started, pandas has been imported as pd, along with the logging module has been imported. The default log-level has been set to "debug"."""

def extract(file_path):
    return pd.read_parquet(file_path)

# Update the pipeline to include a try block
try:
	# Attempt to read in the file
    raw_sales_data = extract("sales_data.parquet")
	
# Catch the FileNotFoundError
except FileNotFoundError as file_not_found:
	# Write an error-level log
	logging.error(file_not_found)


"""Monitoring and alerting within a data pipeline
It's time to put it all together! You might have guessed it, but using handling errors using try-except and logging go hand-in-hand. These two practices are essential for a pipeline to be resilient and transparent, and are the building blocks for more advanced monitoring and alerting solutions.

pandas has been imported as pd, and the logging module has been loaded and configured for you. The raw_sales_data DataFrame has been extracted, and is ready to be transformed."""

def transform(raw_data):
	return raw_data.loc[raw_data["Total Price"] > 1000, :]

try:
	# Attempt to transform DataFrame, log an info-level message
	clean_sales_data = transform(raw_sales_data)
	logging.info("Successfully filtered DataFrame by 'Total Price'")
	
except Exception:
	# Log a warning-level message
	logging.warning("Cannot filter DataFrame by 'Total Price'")


def transform(raw_data):
	return raw_data.loc[raw_data["Total Price"] > 1000, :]

try:
	clean_sales_data = transform(raw_sales_data)
	logging.info("Successfully filtered DataFrame by 'Total Price'")
	
except KeyError as ke:
	logging.warning(f"{ke}: Cannot filter DataFrame by 'Total Price'")
	
	# Create the "Total Price" column, transform the updated DataFrame
	raw_sales_data["Total Price"] = raw_sales_data["Price Each"] * raw_sales_data["Quantity Ordered"]
	clean_sales_data = transform(raw_sales_data)


