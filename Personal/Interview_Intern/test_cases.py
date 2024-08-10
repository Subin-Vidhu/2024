import numpy as np
from PIL import Image
import os

def create_random_image(width, height):
    """Creates a random image with the specified width and height."""
    # Create a 3D numpy array with random values between 0 and 255
    image_array = np.random.randint(0, 256, size=(height, width, 3), dtype=np.uint8)

    # Convert the numpy array to a PIL Image
    image = Image.fromarray(image_array)

    return image

def save_image(image, path):
    """Saves the image to the specified path."""
    # Save the image to the specified path
    image.save(path)

def main():
    # Specify the width and height of the image
    width = 512
    height = 512

    # Specify the path to save the image
    destination = r"D:\2024\Personal\Interview_Intern\sample_data\test_image1.png"

    # Create a random image
    image = create_random_image(width, height)

    # Save the image to the specified path
    save_image(image, destination)

    print(f"Image saved to {destination}")

if __name__ == "__main__":
    main()