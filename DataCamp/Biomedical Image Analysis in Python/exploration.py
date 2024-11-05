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

# Print the image type
print('Image type:', type(im))

#3
# Plot the image
plt.imshow(im, cmap='gray')
plt.axis('off')
plt.show()

#4
# Plot the image with vmin, vmax and cmap - 'gray', here vmin is 40 and vmax is 80, vmin and vmax set the limits of the color scale, meaning that all pixels with values lower than vmin will be black and all pixels with values higher than vmax will be white.
plt.imshow(im, cmap='gray', vmin=40, vmax=80)
plt.axis('off')
plt.show()

#5 - Stack Images
# Import ImageIO and NumPy
import imageio
import numpy as np

# Read in each 2D image
im1 = imageio.imread('chest-220.dcm')
im2 = imageio.imread('chest-221.dcm')
im3 = imageio.imread('chest-222.dcm')

# Stack images into a volume
vol = np.stack([im1,im2,im3])
print('Volume dimensions:', vol.shape)

#6 - Load Volumes
# Import ImageIO
import imageio

# Load the "tcia-chest-ct" directory
vol = imageio.volread('tcia-chest-ct')

# Print image attributes
print('Available metadata:', vol.meta.keys())
print('Shape of image array:', vol.shape)

#7 - SubPlot
# Import PyPlot
import matplotlib.pyplot as plt

# Initialize figure and axes grid
fig, axes = plt.subplots(nrows=2, ncols=1)

# Draw an image on each subplot
axes[0].imshow(im1, cmap='gray')  # Replace image1 with your actual image
axes[0].axis('off')  # Remove ticks and labels

axes[1].imshow(im2, cmap='gray')  # Replace image2 with your actual image
axes[1].axis('off')  # Remove ticks and labels

# Render the plot
plt.show()

# - Slice 3D images
# Initialize figure and axes grid
# Initialize figure and axes grid
fig, axes = plt.subplots(nrows=1, ncols=4)

# Plot every 40th slice of vol in grayscale
for ii in range(4):
    im = vol[ii*40, :, :]
    axes[ii].imshow(im, cmap='gray')
    axes[ii].axis('off')  # Turn off ticks, labels, and frame

# Render the figure
plt.show()

#9 - Plot other views
# Select frame from "vol"
im1 = vol[:, 256, :]
im2 = vol[:, :, 256]

# Compute aspect ratios
d0, d1, d2 = vol.meta['sampling']
asp1 = d0 / d2
asp2 = d0 / d1

# Plot the images on a subplots array 
fig, axes = plt.subplots(nrows=2, ncols=1)
axes[0].imshow(im1, cmap='gray', aspect=asp1)
axes[1].imshow(im2, cmap='gray', aspect=asp2)
plt.show()