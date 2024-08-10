import numpy as np
import logging
from typing import Union

def calculate_mean(numbers: Union[list, np.ndarray]) -> float:
    """
    Calculate the mean of a list of numbers.

    Args:
        numbers: A list or numpy array of numbers.

    Returns:
        The mean of the input numbers.

    Raises:
        ValueError: If the input is not a list or numpy array, or if it is empty.
        TypeError: If the input contains non-numeric values.
    """
    logging.basicConfig(level=logging.INFO)

    if not isinstance(numbers, (list, np.ndarray)):
        logging.error("Input must be a list or numpy array")
        raise ValueError("Input must be a list or numpy array")

    if len(numbers) == 0:
        logging.error("Input list cannot be empty")
        raise ValueError("Input list cannot be empty")

    try:
        mean = np.mean(numbers)
        if np.isnan(mean):
            logging.error("Input contains non-numeric values")
            raise TypeError("Input contains non-numeric values")
    except Exception as e:
        logging.error(f"Failed to calculate mean: {e}")
        raise

    return mean

# Test cases
import unittest

class TestCalculateMean(unittest.TestCase):
    def test_valid_list(self):
        numbers = [1, 2, 3, 4, 5]
        self.assertEqual(calculate_mean(numbers), 3.0)

    def test_valid_numpy_array(self):
        numbers = np.array([1, 2, 3, 4, 5])
        self.assertEqual(calculate_mean(numbers), 3.0)

    def test_empty_list(self):
        numbers = []
        with self.assertRaises(ValueError):
            calculate_mean(numbers)

    def test_non_numeric_values(self):
        numbers = [1, 2, 'a', 4, 5]
        with self.assertRaises(TypeError):
            calculate_mean(numbers)

    def test_non_list_input(self):
        numbers = 'hello'
        with self.assertRaises(ValueError):
            calculate_mean(numbers)

if __name__ == '__main__':
    unittest.main()