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

