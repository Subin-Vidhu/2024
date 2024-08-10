import unittest
from unittest import mock
import requests
from interview_solutions import (
    format_string, print_formatted, celsius_to_fahrenheit, fahrenheit_to_celsius,
    convert_temperatures, fibonacci, is_prime, download_file, download_files_concurrently
)
import io
import sys
import tempfile
import os
import threading

class TestPythonInterviewQuestions(unittest.TestCase):
    def test_format_string(self):
        self.assertEqual(format_string("Hello World", True), "HELLO WORLD")
        self.assertEqual(format_string("Hello World", False), "hello world")
        self.assertEqual(format_string("123!@#$%^&*()_+", True), "123!@#$%^&*()_+")
        self.assertEqual(format_string("", True), "")
        self.assertEqual(format_string("", False), "")
        self.assertEqual(format_string("MiXeD CaSe", True), "MIXED CASE")
        self.assertEqual(format_string("MiXeD CaSe", False), "mixed case")

    def test_print_formatted(self):
        # Redirect stdout to capture print output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        print_formatted(["Hello", "World", "Python"], True)
        self.assertEqual(captured_output.getvalue(), "HELLO\nWORLD\nPYTHON\n")

        captured_output.truncate(0)
        captured_output.seek(0)

        print_formatted(["Hello", "World", "Python"], False)
        self.assertEqual(captured_output.getvalue(), "hello\nworld\npython\n")

        captured_output.truncate(0)
        captured_output.seek(0)

        print_formatted([], True)
        self.assertEqual(captured_output.getvalue(), "")

        # Reset redirect
        sys.stdout = sys.__stdout__

    def test_temperature_converter(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32.00, places=2)
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0.00, places=2)
        self.assertEqual(convert_temperatures([0, 100, -40], 'CtoF'), [32.00, 212.00, -40.00])
        self.assertEqual(convert_temperatures([32, 212, -40], 'FtoC'), [0.00, 100.00, -40.00])
        self.assertAlmostEqual(celsius_to_fahrenheit(37), 98.60, places=2)
        self.assertAlmostEqual(fahrenheit_to_celsius(98.6), 37.00, places=2)
        with self.assertRaises(ValueError):
            convert_temperatures([0, 100], 'InvalidDirection')

    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(20), 6765)
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_prime_check(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertFalse(is_prime(4))
        self.assertTrue(is_prime(29))
        self.assertFalse(is_prime(100))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(97))
        self.assertFalse(is_prime(10000))

    def test_file_downloader(self):
        # Create a temporary directory for test files
        with tempfile.TemporaryDirectory() as temp_dir:
            urls = [
                "https://httpbin.org/image/png",
                "https://httpbin.org/image/jpeg",
                "https://httpbin.org/image/webp"
            ]
            destinations = [
                os.path.join(temp_dir, "file1.png"),
                os.path.join(temp_dir, "file2.jpg"),
                os.path.join(temp_dir, "file3.webp")
            ]

            # Mock the requests.get function to avoid actual network calls
            with unittest.mock.patch('requests.get') as mock_get:
                # Test successful downloads
                mock_response = unittest.mock.Mock()
                mock_response.content = b"Test content"
                mock_response.raise_for_status.return_value = None
                mock_get.return_value = mock_response

                download_files_concurrently(urls, destinations)

                # Check if all files were "downloaded"
                for dest in destinations:
                    self.assertTrue(os.path.exists(dest))
                    with open(dest, 'rb') as f:
                        self.assertEqual(f.read(), b"Test content")

                # Test error handling
                mock_get.side_effect = requests.RequestException("Test error")
                captured_output = io.StringIO()
                sys.stdout = captured_output
                download_files_concurrently(urls, destinations)
                sys.stdout = sys.__stdout__
                self.assertTrue("Error downloading" in captured_output.getvalue())

                # Test with mismatched URLs and destinations
                with self.assertRaises(ValueError):
                    download_files_concurrently(urls, destinations[:-1])

                # Test with empty lists
                download_files_concurrently([], [])

                # Test individual file download with error
                captured_output = io.StringIO()
                sys.stdout = captured_output
                download_file(urls[0], destinations[0])
                sys.stdout = sys.__stdout__
                self.assertTrue("Error downloading" in captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()    