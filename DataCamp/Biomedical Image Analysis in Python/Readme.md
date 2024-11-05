# Field of view
- The `amount of physical space` covered by an image is its `field of view`, which is calculated from two properties:

    - `Array shape`, the number of data elements on each axis. Can be accessed with the shape attribute.

    - `Sampling resolution`, the amount of physical space covered by each pixel. Sometimes available in metadata (e.g., meta['sampling']).

    - eg: `Field of view = Array shape * Sampling resolution`

# Info

- When selecting frames, any trailing : symbols are implicitly selected. For example, vol[5] is the same as vol[5,:,:]

    - `vol[5]` is the same as `vol[5,:,:]`, eg: `vol[5, 10:20, 10:20]` is the same as `vol[5, 10:20, 10:20, :]`

# Histograms

- Histograms display the distribution of values in your image by binning each element by its intensity then measuring the size of each bin.

- The area under a histogram is called the cumulative distribution function. It measures the frequency with which a given range of pixel intensities occurs.
