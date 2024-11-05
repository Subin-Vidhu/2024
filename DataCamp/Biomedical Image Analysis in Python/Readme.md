# Field of view
- The `amount of physical space` covered by an image is its `field of view`, which is calculated from two properties:

    - `Array shape`, the number of data elements on each axis. Can be accessed with the shape attribute.

    - `Sampling resolution`, the amount of physical space covered by each pixel. Sometimes available in metadata (e.g., meta['sampling']).

    - eg: `Field of view = Array shape * Sampling resolution`
    