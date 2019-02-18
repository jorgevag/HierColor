import numpy as np
import matplotlib.pyplot as plt
#from skimage import io
#from skimage.draw import circle_perimeter
from skimage.color import luv2rgb

# Testing LAB to RGV
#from skimage.color import lab2rgb, rgb2gray
#lab2rgb(np.array([[[255, 0, 0]]], dtype=np.uint8))
#red_pixel_rgb = np.array([[[255, 0, 0]]], dtype=np.uint8)

res = 1000 # resolution
restr = 120 # restriction
L = 80


im_luv = np.zeros((res+1, res+1, 3))
#print(np.shape(im_luv))
#print(im_luv)

for i, u in enumerate(range(-res//2, 1+res//2)):
  for j, v in enumerate(range(-res//2, 1+res//2)):
    im_luv[i, j, 0] = L
    im_luv[i, j, 1] = restr*u/res
    im_luv[i, j, 2] = restr*v/res

im_rgb = luv2rgb(im_luv)


#cx, cy = circle_perimeter(res//2, res//2, res//3)
#im_rgb[cx, cy, :] = (0, 0, 0)
#io.imshow(im_rgb)

ax = plt.subplot(aspect='equal')
ax.imshow(im_rgb)


ax.add_artist(
  plt.Circle(xy=(res//2, res//2),
             radius=res//3,
             fill=False,
             alpha=0.5)
)


plt.show()


