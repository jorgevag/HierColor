# Source: https://stackoverflow.com/questions/44497352/printing-colors-on-screen-in-python

import numpy as np

import matplotlib.pyplot as plt

from skimage import io

palette = np.array([[255,   0,   0], # index 0: red
                    [  0, 255,   0], # index 1: green
                    [  0,   0, 255], # index 2: blue
                    [255, 255, 255], # index 3: white
                    [  0,   0,   0], # index 4: black
                    [255, 255,   0], # index 5: yellow
                    ], dtype=np.uint8)


indices = np.random.randint(0, len(palette), size=(4, 6))

io.imshow(palette[indices])
plt.show()

m, n = 100, 100
random = np.uint8(np.random.randint(0, 255, size=(m, n, 3)))
io.imshow(random)
plt.show()
