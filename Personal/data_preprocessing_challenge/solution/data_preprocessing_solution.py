import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer

# Load the dataset from the API
url = "https://www.healthit.gov/data/open-api?source=2015-edition-market-readiness-hospitals-clinicians-data.csv"
df = pd.read_json(url)

# Handle missing values
numerical_imputer = SimpleImputer(strategy='median')
categorical_imputer = SimpleImputer(strategy='most_frequent')

numerical_cols = df.select_dtypes(include=['number']).columns
categorical_cols = df.select_dtypes(include=['object']).columns

df[numerical_cols] = numerical_imputer.fit_transform(df[numerical_cols])
df[categorical_cols] = categorical_imputer.fit_transform(df[categorical_cols])

# Function to handle outliers using IQR method
def handle_outliers(col):
    Q1 = col.quantile(0.25)
    Q3 = col.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return col.clip(lower=lower_bound, upper=upper_bound)

# Apply the outlier handling function to all numerical columns
df[numerical_cols] = df[numerical_cols].apply(handle_outliers)

# Normalize numerical features using Min-Max scaling
scaler = MinMaxScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# Encode categorical variables
for col in categorical_cols:
    if df[col].nunique() < 10:
        # One-hot encoding for low cardinality
        df = pd.get_dummies(df, columns=[col], prefix=col)
    else:
        # Label encoding for high cardinality
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

# Create new feature: certified_to_total_ratio
if 'certifiedProducts' in df.columns and 'totalProducts' in df.columns:
    df['certified_to_total_ratio'] = df['certifiedProducts'] / df['totalProducts']
else:
    print("Warning: 'certifiedProducts' or 'totalProducts' column not found. Skipping ratio calculation.")

# Print summary statistics
print("Summary statistics of preprocessed data:")
print(df.describe())

# Save the preprocessed data to a new CSV file
df.to_csv('preprocessed_health_it_data.csv', index=False)

print("Preprocessing completed. Data saved to 'preprocessed_health_it_data.csv'")
