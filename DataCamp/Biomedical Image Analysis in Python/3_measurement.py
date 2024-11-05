# Segment the heart
# Apply a median filter to im. Set the size to 3.
im_filt = ndi.median_filter(im, size=3)

# Create a mask of values greater than 60
mask_start = np.where(im_filt > 60, 1, 0)
mask = ndi.binary_closing(mask_start)

# Label the objects in "mask"
labels, nlabels = ndi.label(mask)
print('Num. Labels:', nlabels)