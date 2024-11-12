"""Ingesting JSON data with pandas
When developing a data pipeline, you may have to work with non-tabular data and data sources, such as APIs or JSON files. In this exercise, we'll practice extracting data from a JSON file using pandas.

pandas has been imported as pd, and the JSON file you'll ingest is stored at the path "testing_scores.json"."""

def extract(file_path):
  # Read the JSON file into a DataFrame
  return pd.read_json(file_path, orient="records")

# Call the extract function with the appropriate path, assign to raw_testing_scores
raw_testing_scores = extract("testing_scores.json")

# Output the head of the DataFrame
print(raw_testing_scores.head())

"""Reading JSON data into memory
When data is stored in JSON format, it's not always easy to load into a DataFrame. This is the case for the "nested_testing_scores.json" file. Here, the data will have to be manually manipulated before it can be stored in a DataFrame.

To help get you started, pandas has been loaded into the workspace as pd."""

def extract(file_path):
  	# Read the JSON file into a DataFrame, orient by index
	return pd.read_json(file_path, orient="index")

# Call the extract function, pass in the desired file_path
raw_testing_scores = extract("nested_scores.json")
print(raw_testing_scores.head())

# Import the json library
import json

def extract(file_path):
    with open(file_path, "r") as json_file:
        # Load the data from the JSON file
        raw_data = json.load(json_file)
    return raw_data

raw_testing_scores = extract("nested_scores.json")

# Print the raw_testing_scores
print(raw_testing_scores)

"""Iterating over dictionaries
Once JSON data is loaded into a dictionary, you can leverage Python's built-in tools to iterate over its keys and values.

The "nested_school_scores.json" file has been read into a dictionary stored in the raw_testing_scores variable, which takes the following form:

{
    "01M539": {
        "street_address": "111 Columbia Street",
        "city": "Manhattan",
        "scores": {
              "math": 657,
              "reading": 601,
              "writing": 601
        }
  }, ...
}"""

raw_testing_scores_keys = []
raw_testing_scores_values = []

# Iterate through the values of the raw_testing_scores dictionary
for school_id, school_info in raw_testing_scores.items():
	raw_testing_scores_keys.append(school_id)
	raw_testing_scores_values.append(school_info)

print(raw_testing_scores_keys[0:3])
print(raw_testing_scores_values[0:3])

"""Parsing data from dictionaries
When JSON data is loaded into memory, the resulting dictionary can be complicated. Key-value pairs may contain another dictionary, such are called nested dictionaries. These nested dictionaries are frequently encountered when dealing with APIs or other JSON data. In this exercise, you will practice extracting data from nested dictionaries and handling missing values.

The dictionary below is stored in the school variable. Good luck!

{
    "street_address": "111 Columbia Street",
    "city": "Manhattan",
    "scores": {
        "math": 657,
        "reading": 601
    }
}"""

# Parse the street_address from the dictionary
street_address = school.get("street_address")

# Parse the scores dictionary
scores = school.get("scores")

# Try to parse the math, reading and writing values from scores
math_score = scores.get("math", 0)
reading_score = scores.get("reading", 0)
writing_score = scores.get("writing", 0)

print(f"Street Address: {street_address}")
print(f"Math: {math_score}, Reading: {reading_score}, Writing: {writing_score}")

"""Transforming JSON data
Chances are, when reading data from JSON format into a dictionary, you'll probably have to apply some level of manual transformation to the data before it can be stored in a DataFrame. This is common when working with nested dictionaries, which you'll have the opportunity to explore in this exercise.

The "nested_school_scores.json" file has been read into a dictionary available in the raw_testing_scores variable, which takes the following form:

{
    "01M539": {
        "street_address": "111 Columbia Street",
        "city": "Manhattan",
        "scores": {
              "math": 657,
              "reading": 601,
              "writing": 601
        }
  }, ...
}"""

normalized_testing_scores = []

# Loop through each of the dictionary key-value pairs
for school_id, school_info in raw_testing_scores.items():
	normalized_testing_scores.append([
    	school_id,
    	school_info.get("street_address"),  # Pull the "street_address"
    	school_info.get("city"),
    	school_info.get("scores").get("math", 0),
    	school_info.get("scores").get("reading", 0),
    	school_info.get("scores").get("writing", 0),
    ])

print(normalized_testing_scores)

"""Transforming and cleaning DataFrames
Once data has been curated into a cleaned Python data structure, such as a list of lists, it's easy to convert this into a pandas DataFrame. You'll practice doing just this with the data that was curated in the last exercise.

Per usual, pandas has been imported as pd, and the normalized_testing_scores variable stores the list of each schools testing data, as shown below.

[
    ['01M539', '111 Columbia Street', 'Manhattan', 657.0, 601.0, 601.0],
    ...
]   """

# Create a DataFrame from the normalized_testing_scores list
normalized_data = pd.DataFrame(normalized_testing_scores)

# Set the column names
normalized_data.columns = ["school_id", "street_address", "city", "avg_score_math", "avg_score_reading", "avg_score_writing"]

normalized_data = normalized_data.set_index("school_id")
print(normalized_data.head())


"""Filling missing values with pandas
When building data pipelines, it's inevitable that you'll stumble upon missing data. In some cases, you may want to remove these records from the dataset. But in others, you'll need to impute values for the missing information. In this exercise, you'll practice using pandas to impute missing test scores.

Data from the file "testing_scores.json" has been read into a DataFrame, and is stored in the variable raw_testing_scores. In addition to this, pandas has been loaded as pd."""

# Fill NaN values with the average from that column
raw_testing_scores["math_score"] = raw_testing_scores["math_score"].fillna(raw_testing_scores["math_score"].mean())

# Print the head of the raw_testing_scores DataFrame
print(raw_testing_scores.head())

def transform(raw_data):
	raw_data.fillna(
    	value={
			# Fill NaN values with column mean
			"math_score": raw_data["math_score"].mean(),
			"reading_score": raw_data["reading_score"].mean(),
			"writing_score": raw_data["writing_score"].mean()
		}, inplace=True
	)
	return raw_data

clean_testing_scores = transform(raw_testing_scores)

# Print the head of the clean_testing_scores DataFrame
print(clean_testing_scores.head())

"""Grouping data with pandas
The output of a data pipeline is typically a "modeled" dataset. This dataset provides data consumers easy access to information, without having to perform much manipulation. Grouping data with pandas helps to build modeled datasets,

pandas has been imported as pd, and the raw_testing_scores DataFrame contains data in the following form:

              street_address       city  math_score  reading_score  writing_score
01M539   111 Columbia Street  Manhattan       657.0          601.0          601.0
02M294      350 Grand Street  Manhattan       395.0          411.0          387.0
02M308      350 Grand Street  Manhattan       418.0          428.0          415.0"""

def transform(raw_data):
	# Use .loc[] to only return the needed columns
	raw_data = raw_data.loc[:, ["city", "math_score", "reading_score", "writing_score"]]
	
    # Group the data by city, return the grouped DataFrame
	grouped_data = raw_data.groupby(by=["city"], axis=0).mean()
	return grouped_data

# Transform the data, print the head of the DataFrame
grouped_testing_scores = transform(raw_testing_scores)
print(grouped_testing_scores.head())

"""Applying advanced transformations to DataFrames
pandas has a plethora of built-in transformation tools, but sometimes, more advanced logic needs to be used in a transformation. The apply function lets you apply a user-defined function to a row or column of a DataFrame, opening the door for advanced transformation and feature generation.

The find_street_name() function parses the street name from the "street_address", dropping the street number from the string. This function has been loaded into memory, and is ready to be applied to the raw_testing_scores DataFrame."""

def transform(raw_data):
	# Use the apply function to extract the street_name from the street_address
    raw_data["street_name"] = raw_data.apply(
    	# Pass the correct function to the apply method
        find_street_name,
        axis=1
    )
    return raw_data

# Transform the raw_testing_scores DataFrame
cleaned_testing_scores = transform(raw_testing_scores)

# Print the head of the cleaned_testing_scores DataFrame
print(cleaned_testing_scores.head())

"""Loading data to a Postgres database
After data has been extracted from a source system and transformed to align with analytics or reporting use cases, it's time to load the data to a final storage medium. Storing cleaned data in a SQL database makes it simple for data consumers to access and run queries against. In this example, you'll practice loading cleaned data to a Postgres database.

sqlalchemy has been imported, and pandas is available as pd. The first few rows of the cleaned_testing_scores DataFrame are shown below:

             street_address       city  math_score  ... best_score
01M539  111 Columbia Street  Manhattan       657.0      Math
02M545     350 Grand Street  Manhattan       613.0      Math
01M292     220 Henry Street  Manhattan       410.0      Math"""

# Update the connection string, create the connection object to the schools database
db_engine = sqlalchemy.create_engine("postgresql+psycopg2://repl:password@localhost:5432/schools")

# Write the DataFrame to the scores table
cleaned_testing_scores.to_sql(
	name="scores",
	con=db_engine,
	index=False,
	if_exists="replace"
)

"""Validating data loaded to a Postgres Database
In this exercise, you'll finally get to build a data pipeline from end-to-end. This pipeline will extract school testing scores from a JSON file and transform the data to drop rows with missing scores. In addition to this, each will be ranked by the city they are located in, based on their total scores. Finally, the transformed dataset will be stored in a Postgres database.

To give you a head start, the extract() and transform() functions have been built and used as shown below. In addition to this, pandas has been imported as pd. Best of luck!

# Extract and clean the testing scores.
raw_testing_scores = extract("testing_scores.json")
cleaned_testing_scores = transform(raw_testing_scores)"""

def load(clean_data, con_engine):
    clean_data.to_sql(name="scores_by_city", con=con_engine, if_exists="replace", index=True, index_label="school_id")
    
# Call the load function, passing in the cleaned DataFrame
load(cleaned_testing_scores, db_engine)

# Call query the data in the scores_by_city table, check the head of the DataFrame
to_validate = pd.read_sql("SELECT * FROM scores_by_city", con=db_engine)
print(to_validate.head())

