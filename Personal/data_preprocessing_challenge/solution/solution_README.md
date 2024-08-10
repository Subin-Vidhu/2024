# Data Preprocessing Challenge Solution

This README provides instructions on how to set up and run the data preprocessing solution for the HealthIT.gov dataset challenge.

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Setup

1. Clone this repository or download the solution files.

2. Install the required Python packages:

   ```
   pip install pandas numpy scikit-learn requests
   ```

## Running the Solution

1. Open a terminal and navigate to the directory containing the solution files.

2. Run the preprocessing script:

   ```
   python data_preprocessing_solution.py
   ```

3. The script will:
   - Access the dataset from the HealthIT.gov API
   - Perform data cleaning and preprocessing steps
   - Save the preprocessed data to a new CSV file

4. After execution, you will find the preprocessed data in `preprocessed_health_it_data.csv`.

## Solution Overview

The `data_preprocessing_solution.py` script performs the following steps:

1. Loads the dataset from the HealthIT.gov API
2. Handles missing values using median imputation for numerical data and mode imputation for categorical data
3. Detects and handles outliers using the Interquartile Range (IQR) method
4. Normalizes numerical features using Min-Max scaling
5. Encodes categorical variables using one-hot encoding for low cardinality and label encoding for high cardinality
6. Creates a new feature: certified_to_total_ratio
7. Saves the preprocessed data to a CSV file

For more detailed information about the preprocessing steps and their implementation, please refer to the comments in the `data_preprocessing_solution.py` file.
