# Translations
# Find image center of mass
import imageio
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
com = ndi.center_of_mass(im)

# Calculate amount of shift needed
d0 = 128 - com[0]
d1 = 128-com[1]

# Translate the brain towards the center
xfm = ndi.shift(im, shift=[d0,d1])

# Find image center of mass
com = ndi.center_of_mass(im)

# Calculate amount of shift needed
d0 = 128 - com[0]
d1 = 128 - com[1]

# Translate the brain towards the center
xfm = ndi.shift(im, shift=(d0, d1))

# Plot the original and adjusted images
fig, axes = plt.subplots(nrows=2, ncols=1)
axes[0].imshow(im)
axes[0].imshow(xfm)
format_and_render_plot()