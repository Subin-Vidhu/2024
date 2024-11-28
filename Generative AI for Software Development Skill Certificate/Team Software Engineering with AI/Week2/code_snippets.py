# Example 1

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# add inline comments to the bubble_sort function
def bubble_sort(arr):
    n = len(arr)  # Get the length of the array
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already sorted, no need to check them
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap the elements
    return arr  # Return the sorted array


# Example 2

import pandas as pd
import numpy as np

# load weather data
weather_df = pd.DataFrame('april2024_station_data.csv')

# Numpy is faster so convert
wind_speed = df['wind_speed'].to_numpy()
wind_direction = df['wind_direction'].to_numpy()

# Better built in function in np
wind_direction_rad = np.deg2rad(wind_direction)

#########################      inline comments to the code
import pandas as pd
import numpy as np

# Load weather data from a CSV file into a DataFrame
weather_df = pd.DataFrame('april2024_station_data.csv')

# Convert wind speed and wind direction columns to NumPy arrays for faster processing
wind_speed = df['wind_speed'].to_numpy()
wind_direction = df['wind_direction'].to_numpy()

# Convert wind direction from degrees to radians using NumPy's built-in function
wind_direction_rad = np.deg2rad(wind_direction)