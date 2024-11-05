#1
# Import ImageIO
import imageio

# Load "chest-220.dcm"
im = imageio.imread("chest-220.dcm")

# Print image attributes
print('Image type:', type(im))
print('Shape of image array:', im.shape)

#2
# Import ImageIO
import imageio
im = imageio.imread('chest-220.dcm')

# Print the available metadata fields
print(im.meta.keys())