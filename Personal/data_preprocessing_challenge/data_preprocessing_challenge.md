# 1-Hour Data Preprocessing Challenge

## Introduction
This challenge is designed to test your ability to quickly understand requirements, implement data preprocessing techniques, and follow detailed instructions. You will be working with a real-world healthcare dataset and performing various data cleaning and preparation tasks. This challenge will evaluate your skills in data manipulation, handling missing values, and preparing data for analysis.

## Task Description
You are tasked with preprocessing the "2015 Edition Market Readiness for Hospitals and Clinicians Data" dataset from HealthIT.gov. Your goal is to clean the data, handle missing values, detect outliers, normalize numerical features, and encode categorical variables. The preprocessed data should be ready for use in a machine learning model (although building the model is not part of this challenge).

## Instructions
1. Access the dataset using the HealthIT.gov API.
   - Base API URL: https://www.healthit.gov/data/open-api?source=2015-edition-market-readiness-hospitals-clinicians-data.csv
2. Load the data into a pandas DataFrame.
3. Perform the following preprocessing steps:
   a. Handle missing values:
      - For numerical columns, impute missing values with the median.
      - For categorical columns, impute missing values with the mode.
   b. Detect and handle outliers:
      - Use the Interquartile Range (IQR) method to detect outliers in numerical columns.
      - Replace outliers with the upper or lower bound as appropriate.
   c. Normalize numerical features:
      - Use Min-Max scaling to normalize all numerical features to a range of [0, 1].
   d. Encode categorical variables:
      - Use one-hot encoding for categorical variables with low cardinality (less than 10 unique values).
      - Use label encoding for categorical variables with high cardinality.
   e. Create a new feature:
      - Calculate the ratio of certified to total products for each vendor.
4. Provide summary statistics of the preprocessed data.
5. Save the preprocessed data to a new CSV file.

## Dataset Information
Dataset: 2015 Edition Market Readiness for Hospitals and Clinicians Data
API Documentation: https://www.healthit.gov/data/open-api

## Required Libraries
- pandas
- numpy
- scikit-learn
- requests

To install the required libraries, run the following command:
```
pip install pandas numpy scikit-learn requests
```

## Submission Guidelines
1. Create a Python script named `preprocess_health_it_data.py` that performs all the required preprocessing steps.
2. Include comments in your code explaining your approach and any assumptions made.
3. Generate a brief report (in Markdown or PDF format) summarizing the preprocessing steps and any insights gained from the data.
4. Submit both the Python script and the report.

## Evaluation Criteria
Your submission will be evaluated based on the following criteria:
1. Correctness: Does the script run without errors and produce the expected output?
2. Code Quality: Is the code well-organized, readable, and properly commented?
3. Efficiency: Does the script handle the preprocessing tasks in a reasonable amount of time?
4. Completeness: Have all required preprocessing steps been implemented?
5. Insights: Does the report provide meaningful insights about the data and preprocessing steps?

Remember, you have 1 hour to complete this challenge. Good luck!

## Resources
- HealthIT.gov API Documentation: https://www.healthit.gov/data/open-api
- Pandas Documentation: https://pandas.pydata.org/docs/
- Scikit-learn Documentation: https://scikit-learn.org/stable/documentation.html

# Data Preprocessing Challenge Solution Documentation

## Introduction
This document summarizes the preprocessing steps, insights, and outcomes of the Data Preprocessing Challenge for the "2015 Edition Market Readiness for Hospitals and Clinicians Data" dataset from HealthIT.gov.

## Dataset Overview
The dataset contains information about the market readiness of hospitals and clinicians for the 2015 Edition of Health IT certification. It includes various metrics related to healthcare providers, market share, and certification status.

## Preprocessing Steps
1. Data Loading: The dataset was accessed using the HealthIT.gov API and loaded into a pandas DataFrame.

2. Handling Missing Values:
   - Numerical columns: Missing values were imputed with the median.
   - Categorical columns: Missing values were imputed with the mode.

3. Outlier Detection and Handling:
   - The Interquartile Range (IQR) method was used to detect outliers in numerical columns.
   - Outliers were replaced with the upper or lower bounds as appropriate.

4. Normalization of Numerical Features:
   - Min-Max scaling was applied to normalize all numerical features to a range of [0, 1].

5. Encoding Categorical Variables:
   - One-hot encoding was used for categorical variables with low cardinality (less than 10 unique values).
   - Label encoding was applied for categorical variables with high cardinality.

6. Feature Creation:
   - A new feature called "market_impact_index" was created, combining provider count, market share, and estimated MIPS 2018 values.

## Descriptive Statistics
Descriptive statistics were generated after each preprocessing step to monitor the changes in the data distribution. These statistics provided insights into the impact of each preprocessing technique on the dataset.

## Conclusion
The preprocessing steps have prepared the dataset for further analysis or machine learning tasks. The data is now clean, normalized, and encoded, with outliers handled and missing values imputed. The creation of the "market_impact_index" feature provides a composite metric that could be valuable for assessing the overall market impact of different healthcare providers.

The preprocessed data has been saved to a new CSV file, ready for use in subsequent analysis or modeling tasks.
