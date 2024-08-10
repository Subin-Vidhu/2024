import unittest
import numpy as np
from testcase import calculate_mean  # Replace 'your_module' with the actual name of your module

class TestCalculateMean(unittest.TestCase):
    def test_valid_list(self):
        numbers = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(calculate_mean(numbers), 3.0)

    def test_valid_numpy_array(self):
        numbers = np.array([1, 2, 3, 4, 5])
        self.assertAlmostEqual(calculate_mean(numbers), 3.0)

    def test_empty_list(self):
        numbers = []
        with self.assertRaises(ValueError):
            calculate_mean(numbers)

    def test_non_numeric_values_in_list(self):
        numbers = [1, 2, 'a', 4, 5]
        with self.assertRaises(TypeError):
            calculate_mean(numbers)

    def test_non_list_input(self):
        numbers = 'hello'
        with self.assertRaises(ValueError):
            calculate_mean(numbers)

    def test_list_with_non_numeric_values(self):
        numbers = [1, 2, None, 4, 5]
        with self.assertRaises(TypeError):
            calculate_mean(numbers)

    def test_numpy_array_with_non_numeric_values(self):
        numbers = np.array([1, 2, np.nan, 4, 5])
        with self.assertRaises(TypeError):
            calculate_mean(numbers)

    def test_input_type_validation(self):
        numbers = 123  # Not a list or numpy array
        with self.assertRaises(ValueError):
            calculate_mean(numbers)

if __name__ == '__main__':
    unittest.main()