"""Dropping missing data
Now that you've explored the volunteer dataset and understand its structure and contents, it's time to begin dropping missing values.

In this exercise, you'll drop both columns and rows to create a subset of the volunteer dataset."""

# Drop the Latitude and Longitude columns from volunteer
volunteer_cols = volunteer.drop(["Latitude", "Longitude"], axis=1)

# Drop rows with missing category_desc values from volunteer_cols
volunteer_subset = volunteer_cols.dropna(subset=["category_desc"])

# Print out the shape of the subset
print(volunteer_subset.shape)

"""Exploring data types
Taking another look at the dataset comprised of volunteer information from New York City, you want to know what types you'll be working with as you start to do more preprocessing.

Which data types are present in the volunteer dataset?"""

"""Converting a column type
If you take a look at the volunteer dataset types, you'll see that the column hits is type object. But, if you actually look at the column, you'll see that it consists of integers. Let's convert that column to type int."""

# Print the head of the hits column
print(volunteer["hits"].head())

# Convert the hits column to type int
volunteer["hits"] = volunteer["hits"].astype("int")

# Look at the dtypes of the dataset
print(volunteer.dtypes)

"""Class imbalance
In the volunteer dataset, you're thinking about trying to predict the category_desc variable using the other features in the dataset. First, though, you need to know what the class distribution (and imbalance) is for that label.

Which descriptions occur less than 50 times in the volunteer dataset?"""

"""Stratified sampling
You now know that the distribution of class labels in the category_desc column of the volunteer dataset is uneven. If you wanted to train a model to predict category_desc, you'll need to ensure that the model is trained on a sample of data that is representative of the entire dataset. Stratified sampling is a way to achieve this!"""

# Create a DataFrame with all columns except category_desc
X = volunteer.drop("category_desc", axis=1)

# Create a category_desc labels dataset
y = volunteer[["category_desc"]]

# Use stratified sampling to split up the dataset according to the y dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# Print the category_desc counts from y_train
print(y_train["category_desc"].value_counts())

