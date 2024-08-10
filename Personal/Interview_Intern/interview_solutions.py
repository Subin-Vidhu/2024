# 1. String Formatter
def format_string(s, flag):
    """Formats a string to uppercase or lowercase."""
    return s.upper() if flag else s.lower()

def print_formatted(strings, flag):
    """Prints a list of strings in uppercase or lowercase."""
    for s in strings:
        print(format_string(s, flag))

# 2. Temperature Converter
def celsius_to_fahrenheit(celsius):
    """Converts Celsius to Fahrenheit."""
    return round((celsius * 9/5) + 32, 2)

def fahrenheit_to_celsius(fahrenheit):
    """Converts Fahrenheit to Celsius."""
    return round((fahrenheit - 32) * 5/9, 2)

def convert_temperatures(temperatures, direction):
    """Converts a list of temperatures from Celsius to Fahrenheit or vice versa."""
    if direction == 'CtoF':
        return [celsius_to_fahrenheit(temp) for temp in temperatures]
    elif direction == 'FtoC':
        return [fahrenheit_to_celsius(temp) for temp in temperatures]
    else:
        raise ValueError("Invalid direction. Use 'CtoF' or 'FtoC'.")

# 3. Fibonacci Sequence
def fibonacci(n):
    """Calculates the nth Fibonacci number."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# 4. Prime Number Check
def is_prime(n):
    """Checks if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 5. Multi-threaded File Downloader
import requests
import threading
import os

def download_file(url, destination):
    """Downloads a file from a URL to a destination path."""
    try:
        # Create the directory if it does not exist
        dir_name = os.path.dirname(destination)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Download the file
        response = requests.get(url)
        response.raise_for_status()

        # Save the file
        with open(os.path.abspath(destination), 'wb') as file:  # Added closing parenthesis
            file.write(response.content)

        # Check if the file was saved successfully
        if not os.path.exists(os.path.abspath(destination)):
            print(f"Error saving file {destination}: file not found")
            return

        print(f"Downloaded: {url} to {destination}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except IOError as e:
        print(f"Error saving file {destination}: {e}")

def download_files_concurrently(urls, destinations):
    """Downloads files concurrently using multiple threads."""
    if len(urls) != len(destinations):
        raise ValueError("The number of URLs must match the number of destinations")

    threads = []
    for url, dest in zip(urls, destinations):
        thread = threading.Thread(target=download_file, args=(url, dest))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Test functions
def test_string_formatter():
    """Tests the string formatter function."""
    assert format_string("Hello World", True) == "HELLO WORLD"
    assert format_string("Hello World", False) == "hello world"
    assert format_string("123!@#$%^&*()_+", True) == "123!@#$%^&*()_+"
    print("String Formatter tests passed")

def test_temperature_converter():
    """Tests the temperature converter functions."""
    assert celsius_to_fahrenheit(0) == 32.00
    assert fahrenheit_to_celsius(32) == 0.00
    assert convert_temperatures([0, 100, -40], 'CtoF') == [32.00, 212.00, -40.00]
    assert convert_temperatures([32, 212, -40], 'FtoC') == [0.00, 100.00, -40.00]
    print("Temperature Converter tests passed")

def test_fibonacci():
    """Tests the Fibonacci function."""
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
    print("Fibonacci tests passed")

def test_prime_check():
    """Tests the prime number check function."""
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False
    assert is_prime(29) == True
    assert is_prime(100) == False
    print("Prime Number Check tests passed")

def test_file_downloader():
    """Tests the multi-threaded file downloader function."""
    urls = [
        "https://httpbin.org/image/png",
        "https://httpbin.org/image/jpeg",
        "https://httpbin.org/image/webp"
    ]
    destinations = [
        r"D:\2024\Personal\Interview_Intern\sample_data/test_image1.png",
        r"D:\2024\Personal\Interview_Intern\sample_data/test_image2.jpg",
        r"D:\2024\Personal\Interview_Intern\sample_data/test_image3.webp"
    ]
    download_files_concurrently(urls, destinations)
    for dest in destinations:
        assert os.path.exists(dest)
        assert os.path.getsize(dest) > 0
        # os.remove(dest)
    print("Multi-threaded File Downloader tests passed")

if __name__ == "__main__":
    test_string_formatter()
    test_temperature_converter()
    test_fibonacci()
    test_prime_check()
    # Uncomment the following line to test the file downloader (requires internet connection)
    test_file_downloader()
    print("All tests passed successfully!")