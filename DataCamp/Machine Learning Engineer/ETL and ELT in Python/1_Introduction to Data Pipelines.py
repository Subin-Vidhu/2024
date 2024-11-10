"""Running an ETL Pipeline
Ready to run your first ETL pipeline? Let's get to it!

Here, the functions extract(), transform(), and load() have been defined for you. To run this data ETL pipeline, you're going to execute each of these functions. If you're curious, take a peek at what the extract() function looks like.

def extract(file_name):
    print(f"Extracting data from {file_name}")
    return pd.read_csv(file_name)"""

# Extract data from the raw_data.csv file
extracted_data = extract(file_name="raw_data.csv")

# Transform the extracted_data
transformed_data = transform(data_frame=extracted_data)

# Load the transformed_data to cleaned_data.csv
load(data_frame=transformed_data, target_table="cleaned_data")

"""ELT in Action
Feeling pretty good about running ETL processes? Well, it's time to give ELT pipelines a try. Like before, the extract(), load(), and transform() functions have been defined for you; all you'll have to worry about is running these functions. Good luck!"""

# Extract data from the raw_data.csv file
raw_data = extract(file_name="raw_data.csv")

# Load the extracted_data to the raw_data table
load(data_frame=raw_data, table_name="raw_data")

# Transform data in the raw_data table
transform(
  source_table="raw_data", 
  target_table="cleaned_data"
)

"""Building an ETL Pipeline
Ready to ratchet up the fun? In this exercise, you'll be responsible for building the rest of the load() function before running each step in the ETL process. The extract() and transform() functions have been defined for you. Good luck!"""

def load(data_frame, file_name):
  # Write cleaned_data to a CSV using file_name
  data_frame.to_csv(file_name)
  print(f"Successfully loaded data to {file_name}")

extracted_data = extract(file_name="raw_data.csv")

# Transform extracted_data using transform() function
transformed_data = transform(data_frame=extracted_data)

# Load transformed_data to the file transformed_data.csv
load(data_frame=transformed_data, file_name="transformed_data.csv")

"""The "T" in ELT
Let's not forget about ELT! Here, the extract() and load() functions have been defined for you. Now, all that's left is to finish defining the transform() function and run the pipeline. Go get 'em!"""

# Complete building the transform() function
def transform(source_table, target_table):
  data_warehouse.execute(f"""
  CREATE TABLE {target_table} AS
      SELECT
          CONCAT("Product ID: ", product_id),
          quantity * price
      FROM {source_table};
  """)

extracted_data = extract(file_name="raw_sales_data.csv")
load(data_frame=extracted_data, table_name="raw_sales_data")

# Populate total_sales by transforming raw_sales_data
transform(source_table="raw_sales_data", target_table="total_sales")

"""Extracting, Transforming, and Loading Student Scores Data
Alright, it's time to build your own ETL pipeline from scratch. In this exercise, you'll build three functions; extract(), transform(), and load(). Then, you'll use these functions to run your pipeline.

The pandas library has been imported as pd. Enjoy!"""

def extract(file_name):
  return pd.read_csv(file_name)

def transform(data_frame):
  return data_frame.loc[:, ["industry_name", "number_of_firms"]]

def load(data_frame, file_name):
  data_frame.to_csv(file_name)
  
extracted_data = extract(file_name="raw_industry_data.csv")
transformed_data = transform(data_frame=extracted_data)

# Pass the transformed_data DataFrame to the load() function
load(data_frame=transformed_data, file_name="number_of_firms.csv")


