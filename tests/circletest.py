import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi


#circle = plt.Circle((10, 10), 2, color='g', clip_on=False, fill=False)
'''
xy  - tuple: (x, y) 
radius=
kwargs**:
color color
alpha float
facecolor
edgecolor
fill
linestyle
linewidth
'''
 

##ax = plt.gca()
#ax=plt.subplot(aspect='equal')
#ax.cla() # clear things for fresh plot
#
## change default range so that new circles will work
#ax.set_xlim((0, 10))
#ax.set_ylim((0, 10))
## some data
#ax.plot(range(11), 'o', color='black')
## key data point that we are encircling
#ax.plot((5), (5), 'o', color='y')
#
#ax.add_artist(circle)
#plt.show()


def rec_plot_circles(x=0, y=0, th=0, r=1, hier=('0', []), ax=None):
  curr_id = hier[0]
  children = hier[-1]
  num_children = len(children)

  # Plot current point
  ax.scatter(x, y)
  
  # Plot circle
  if children:
    ax.add_artist(
      plt.Circle(xy = (x, y), 
                 radius = r,
                 fill = False, 
                 alpha = 0.5
      )
    )

    # repeat for every child
    ## define angles 
    delta = 2*pi/num_children

    def is_odd(number):
      return (number % 2) != 0

    if is_odd(num_children):
      angle_shift = 0.0
    else:
      angle_shift = delta/2.0

    ## define new radius:
    ### arc length approximation:
    #child_r = 2*pi/(3*num_children)
    ### loc: law of cosines (correct)
    loc_angle = 2*pi/(3*num_children)
    child_r_squared = 2*(r**2)*(1 - np.cos(loc_angle))
    child_r = np.sqrt(child_r_squared)
    child_r = 0.80*child_r # Shrink radius by a factor (tunable)

    for i, child in enumerate(children):
      child_th = th + i*delta + angle_shift
      child_x = r*np.cos(child_th)
      child_y = r*np.sin(child_th)
      rec_plot_circles(
        x   = x + child_x,
        y   = y + child_y,
        th  = child_th,
        r   = child_r,
        hier=child,
        ax  =ax,
      )

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
  ('3', [])
])

ax = plt.subplot(aspect='equal')
ax.cla()
rec_plot_circles(x=0, y=0, th=0, r=1, hier=hier0, ax=ax)

ax.set_xlim((-2, 2))
ax.set_ylim((-2, 2))
#plt.show()



def print_hier(hier=None, level=0):
  """
  Assumes children nodes are given as the final element of the tuple as a list
  """
  if not hier:
    print("Error print_hier(hier):: no input hierarchy given!")
    return
  
  children = hier[-1]
  indent = 2*level*' '
  line = indent+'('
  for i in range(len(hier)-1):
    line += str(hier[i])+', '
  if children:
    print(line+'[')
    for child in children:
      print_hier(child, level=level+1)
    print(indent+'])')
  else:
    print(line+'[])')

def count_hier(hier):
  curr_id = hier[0]
  children = hier[-1]
  num_children = len(children)

  count = 0
  counted_children = []
  if children:
    for i, child in enumerate(children):
      counted_child = count_hier(child)
      count += 1 + counted_child[1]
      counted_children += [counted_child]
       
  return (hier[0], count, counted_children)

counted_hier = count_hier(hier0)
print()
print_hier(counted_hier)


def rec_plot_weighted_circles(x=0, y=0, th=0, r=1, hier=('0', []), ax=None):
  """
  NOT FINISHED
  * I havent found a way to distribute the available space
    to the points based on the points' "weights"=number of 
    subnodes
  * how do i do dis?
  """

  curr_id = hier[0]
  children = hier[-1]
  num_children = len(children)

  hier = count_hier(hier)
  child_weights = []
  for child in children:
    cild_weights += [child[1]]

  # Plot current point
  ax.scatter(x, y)
  
  # Plot circle
  if children:
    ax.add_artist(
      plt.Circle(xy = (x, y), 
                 radius = r,
                 fill = False, 
                 alpha = 0.5
      )
    )

    # repeat for every child
    ## define angles 
    delta = 2*pi/num_children

    def is_odd(number):
      return (number % 2) != 0

    if is_odd(num_children):
      angle_shift = 0.0
    else:
      angle_shift = delta/2.0

    ## define new radius:
    ### arc length approximation:
    #child_r = 2*pi/(3*num_children)
    ### loc: law of cosines (correct)
    loc_angle = 2*pi/(3*num_children)
    child_r_squared = 2*(r**2)*(1 - np.cos(loc_angle))
    child_r = np.sqrt(child_r_squared)
    child_r = 0.80*child_r # Shrink radius by a factor (tunable)

    for i, child in enumerate(children):
      child_th = th + i*delta + angle_shift
      child_x = r*np.cos(child_th)
      child_y = r*np.sin(child_th)
      rec_plot_circles(
        x   = x + child_x,
        y   = y + child_y,
        th  = child_th,
        r   = child_r,
        hier=child,
        ax  =ax,
      )







def hier_to_table(hier):
  """convert hierarchy to a table format"""
  curr_id = hier[0]
  children = hier[-1]

  if children:
    subtables = []
    subtable_widths = []
    for i, child in enumerate(children):
      subtable = hier_to_table(child)
      subtable_widths += [len(subtable[0])]
      subtables += [subtable]
    max_subtable_width = max(subtable_widths)    
    
    table = []
    for subtable, subtable_width in zip(subtables, subtable_widths):
      left_fill = (max_subtable_width - subtable_width)*['?']
      for row in subtable:
        table_row = [[curr_id] + row + left_fill]
        table += table_row
  else:
    table = [[curr_id]]
  return table

def print_table(table):
  for row in table:
    print(row)
    
table0 = hier_to_table(hier0)
counts_table = hier_to_table(counted_hier)

    
print('print list-table using print_table()')
print_table(table0)
print()
print_table(counts_table)
print()


print('print list-table as pandas DataFrame')
import pandas as pd
print(pd.DataFrame(table0))
print()

