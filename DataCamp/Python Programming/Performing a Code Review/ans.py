import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def prepare_smartphone_data(file_path):
    """
    To prepare the smartphone data for visualization, a number of transformations 
    will be applied after reading in the raw DataFrame to memory, including:
        - reducing the number of columns to only those needed for later analysis
        - removing records without a battery_capacity value
        - divide the price column by 100 to find the dollar amount
    
    :param file_path: the file path where the raw smartphone data is stored
    :return: a cleaned dataset having had the operations above applied to it
    """
    
    # Check if file exists before proceeding
    if os.path.exists(file_path):
        raw_data = pd.read_csv(file_path)
        # Update 1: Variable name 'raw Data' changed to 'raw_data' for Python snake_case naming convention.
    else:
        raise Exception(f"File not found at {file_path}")

    # Keep only necessary columns for analysis
    feature_set = [
        "brand_name",
        "os",
        "price",
        "avg_rating",
        "processor_speed",
        "battery_capacity",
        "screen_size"
    ]
    # Update 2: Renamed 'columns_to_keep_in_clean data' to 'feature_set' for clarity and succinctness.
    clean_data = raw_data.loc[:, feature_set]
    
    # Remove entries without 'battery_capacity' or 'os'
    clean_data = clean_data.dropna(subset=["battery_capacity", "os"])
    # Update 3: Adjusted spacing in 'dropna' function call to improve readability.
    
    # Convert 'price' column to reflect dollar amounts
    clean_data["price"] = clean_data["price"] / 100
    # Update 4: Added spaces around '/' operator for better code readability.
    
    return clean_data

# Prepare the data
cleaned_data = prepare_smartphone_data("./data/smartphones.csv")

def column_to_label(column_name):
    """
    Converts a column name in a pandas DataFrame to a string that can be
    used as a label in a plot.
    
    :param column_name: string containing original column name
    :return: string that is ready to be presented on a plot
    """
    
    if isinstance(column_name, str):
        return " ".join(column_name.split("_")).title()
        # Update 5: Encapsulated logic into 'column_to_label' function to promote DRY principle.
    else:
        raise Exception("Column name must be a string.")

def visualize_versus_price(clean_data, x):
    """
    Use seaborn and matplotlib to identify a pattern between price and 
    processor_speed.
    
    :param clean_data: a pandas DataFrame containing cleaned smartphone data
    :param x: variable to be plotted on the x-axis
    :return: None
    """
    
    x_title = column_to_label(x)
    # Update 6: Used 'column_to_label' function to remove duplicated code.
    
    sns.scatterplot(x=x, y="price", data=clean_data, hue="os")
    plt.xlabel(x_title)
    plt.ylabel("Price ($)")
    plt.title(f"{x_title} vs. Price")

# Visualize the data
visualize_versus_price(cleaned_data, "processor_speed")

# Testing setup
import pytest
import ipytest

ipytest.config.rewrite_asserts = True
__file__ = "notebook.ipynb"

@pytest.fixture()
def clean_smartphone_data():
    return prepare_smartphone_data("./data/smartphones.csv")
    
def test_nan_values(clean_smartphone_data):
    """
    Ensures no NaN values in critical columns.
    """
    
    assert clean_smartphone_data["battery_capacity"].isnull().sum() == 0
    assert clean_smartphone_data["os"].isnull().sum() == 0
    # Update 7: Corrected logical error by ensuring correct assertion syntax for checking NaN values.
