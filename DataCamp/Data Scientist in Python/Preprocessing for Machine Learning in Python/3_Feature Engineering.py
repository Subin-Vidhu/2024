"""Encoding categorical variables - binary
Take a look at the hiking dataset. There are several columns here that need encoding before they can be modeled, one of which is the Accessible column. Accessible is a binary feature, so it has two values, Y or N, which need to be encoded into 1's and 0's. Use scikit-learn's LabelEncoder method to perform this transformation."""

# Set up the LabelEncoder object
enc = LabelEncoder()

# Apply the encoding to the "Accessible" column
hiking["Accessible_enc"] = enc.fit_transform(hiking["Accessible"])

# Compare the two columns
print(hiking[["Accessible_enc", "Accessible"]].head())

"""Encoding categorical variables - one-hot
One of the columns in the volunteer dataset, category_desc, gives category descriptions for the volunteer opportunities listed. Because it is a categorical variable with more than two categories, we need to use one-hot encoding to transform this column numerically. Use pandas' pd.get_dummies() function to do so."""

# Transform the category_desc column
category_enc = pd.get_dummies(volunteer["category_desc"])

# Take a look at the encoded columns
print(category_enc.head())

"""Aggregating numerical features
A good use case for taking an aggregate statistic to create a new feature is when you have many features with similar, related values. Here, you have a DataFrame of running times named running_times_5k. For each name in the dataset, take the mean of their 5 run times."""

# Use .loc to create a mean column
running_times_5k["mean"] = running_times_5k.loc[:, "run1":"run5"].mean(axis=1)

# Take a look at the results
print(running_times_5k.head())

"""Extracting datetime components
There are several columns in the volunteer dataset comprised of datetimes. Let's take a look at the start_date_date column and extract just the month to use as a feature for modeling."""

# First, convert string column to date column
volunteer["start_date_converted"] = pd.to_datetime(volunteer["start_date_date"])

# Extract just the month from the converted column
volunteer["start_date_month"] = volunteer["start_date_converted"].dt.month

# Take a look at the converted and new month columns
print(volunteer[["start_date_converted", "start_date_month"]].head())

"""Extracting string patterns
The Length column in the hiking dataset is a column of strings, but contained in the column is the mileage for the hike. We're going to extract this mileage using regular expressions, and then use a lambda in pandas to apply the extraction to the DataFrame."""

# Write a pattern to extract numbers and decimals
def return_mileage(length):
    
    # Search the text for matches
    mile = re.search("\d+\.\d+", length)
    
    # If a value is returned, use group(0) to return the found value
    if mile is not None:
        return float(mile.group(0))
        
# Apply the function to the Length column and take a look at both columns
hiking["Length_num"] = hiking["Length"].apply(return_mileage)
print(hiking[["Length", "Length_num"]].head())

"""Vectorizing text
You'll now transform the volunteer dataset's title column into a text vector, which you'll use in a prediction task in the next exercise."""

# Take the title text
title_text = volunteer["title"]

# Create the vectorizer method
tfidf_vec = TfidfVectorizer()

# Transform the text into tf-idf vectors
text_tfidf = tfidf_vec.fit_transform(title_text)

"""Text classification using tf/idf vectors
Now that you've encoded the volunteer dataset's title column into tf/idf vectors, you'll use those vectors to predict the category_desc column."""

# Split the dataset according to the class distribution of category_desc
y = volunteer["category_desc"]
X_train, X_test, y_train, y_test = train_test_split(text_tfidf.toarray(), y, stratify=y, random_state=42)

# Fit the model to the training data
nb.fit(X_train, y_train)

# Print out the model's accuracy
print(nb.score(X_test, y_test))

