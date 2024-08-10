import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Read the JSON dataset
df = pd.read_json('healthcare_dataset.csv')

# Function to handle outliers using IQR method
def handle_outliers(col):
    Q1 = col.quantile(0.25)
    Q3 = col.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return col.clip(lower=lower_bound, upper=upper_bound)

# Apply the outlier handling function to all numerical columns
numerical_cols = df.select_dtypes(include=['number']).columns
df[numerical_cols] = df[numerical_cols].apply(handle_outliers)

# Print descriptive statistics after handling outliers
print("Descriptive statistics after handling outliers:")
print(df.describe(include='all'))

# Normalize numerical features using Min-Max scaling
scaler = MinMaxScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# Print descriptive statistics after normalization
print("\nDescriptive statistics after normalization:")
print(df.describe(include='all'))

# Encode categorical variables
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if df[col].nunique() < 10:
        # One-hot encoding for low cardinality
        df = pd.get_dummies(df, columns=[col], prefix=col)
    else:
        # Label encoding for high cardinality
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

# Print descriptive statistics after encoding
print("\nDescriptive statistics after encoding:")
print(df.describe(include='all'))

# Create new feature: market_impact_index
df['market_impact_index'] = (
    0.5 * df['provider_count'] +
    0.3 * df['mktShare'] +
    0.2 * df['est_mips_2018']
)

# Print descriptive statistics after creating new feature
print("\nDescriptive statistics after creating market_impact_index:")
print(df.describe(include='all'))

# Save the cleaned, normalized, and encoded DataFrame to a CSV file
df.to_csv('healthcare_dataset_cleaned_normalized_encoded.csv', index=False)
