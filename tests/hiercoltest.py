import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi
from skimage.color import luv2rgb

res = 1000 # resolution
restr = 120 # restriction
L = 70


# Generate Background Image in RGB colors
im_luv = np.zeros((res+1, res+1, 3))
for i, u in enumerate(range(-res//2, 1+res//2)):
  for j, v in enumerate(range(-res//2, 1+res//2)):
    im_luv[i, j, 0] = L*0.90
    im_luv[i, j, 1] = restr*u/res
    im_luv[i, j, 2] = restr*v/res
im_rgb = luv2rgb(im_luv)


ax = plt.subplot(aspect='equal')
ax.imshow(im_rgb)

def is_odd(number):
  return (number % 2) != 0

#def rec_plot_circles(x=0, y=0, th=0, r=1, hier=('0', []), ax=None):
def rec_plot_circles(x=0, y=0, th=0, r=1, hier=('0', []), ax=None, lL=50, lres=1000, lrestr=120):
  curr_id = hier[0]
  children = hier[-1]
  num_children = len(children)

  # Plot current point
  print(luv2rgb([[[lL, (x/lres)*lrestr, (y/lres)*lrestr]]])[0])
  col_x = restr * (x - lres//2) / res
  col_y = restr * (y - lres//2) / res

  ax.scatter(x, y,  c=luv2rgb([[[lL, col_y, col_x]]])[0], alpha=1, s=200, edgecolor='k')
  
  # Plot circle
  if children:
    ax.add_artist(
      plt.Circle(xy = (x, y), 
                 radius = r,
                 fill = False, 
                 alpha = 0.5
      )
    )

    # for every child
    ## define angles 
    delta = 2*pi/num_children

    if is_odd(num_children):
      angle_shift = 0.0
    else:
      angle_shift = delta/2.0

    ## define new radius with law of cosines (correct) (circle segment split in 3)
    loc_angle = 2*pi/(3*num_children)
    child_r_squared = 2*(r**2)*(1 - np.cos(loc_angle))
    child_r = np.sqrt(child_r_squared)
    child_r = 0.80*child_r # Shrink radius by a factor (tunable)

    for i, child in enumerate(children):
      child_th = th + i*delta + angle_shift
      child_x = r*np.cos(child_th)
      child_y = r*np.sin(child_th)
      # Plot an extract coordinates
      coordinates = rec_plot_circles(x     = x + child_x,
                                     y     = y + child_y,
                                     th    = child_th,
                                     r     = child_r,
                                     hier  = child,
                                     ax    = ax, 
                                     lL     = lL,
                                     lres   = lres,
                                     lrestr = lrestr)
    return [[x, y]] + coordinates
  else: # No Children
    return [[x, y]]


hier0 = ('0', [
  ('1', [
     ('11', []),
     ('12', []),
     ('13', [
       ('131', []),
       ('132', [
         ('1321', [
           ('13211', []),
           ('13212', []),
           ('13213', []),
           ('13214', []),
           ('13215', [])
         ]),
         ('1322', []),
         ('1323', []),
         ('1324', []),
       ]),
       ('133', [])
     ]),
     ('14', [])
  ]),
  ('2', []), 
  ('3', [
     ('31', [
       ('311', []),
       ('312', [])
     ]),
     ('32', [])
  ])
])

coordinates = rec_plot_circles(x=res//2, y=res//2, th=0, r=res/3.0, hier=hier0, ax=ax, lL=L, lres=res, lrestr=restr)

plt.show()


