import numpy as np
import pandas as pd
from io import StringIO

import json

from scipy.constants import pi
from skimage.color import luv2rgb

"""
 NOTE: the hierarchy nodes can have only 1 missing type child,
       (another missing would be included in group).
"""

def print_json(input_json):
  # If str-json, convertto dict
  if isinstance(input_json, str):
    input_json = json.loads(input_json)

  print(json.dumps(input_json,
                   indent=2,
                   sort_keys=True))

def print_hier(hier, level=0, indent='   '):
  if hier:
    print(level*indent + '{value : '   + str(hier['value']))
    #print(level*indent + ' color : '   + str(hier['color']))
    #print(level*indent + ' subnodes : '+ str(hier['subnodes']))
    #print(level*indent + ' subsum : '  + str(hier['subsum']))
    if hier['children']:
      print(level*indent + ' children : [')
      for child in hier['children']:
        print_hier(child, level=level+1, indent=indent)
      print(level*indent + ']}')
    else:
      print(level*indent + ' children : []}')
  else:
    print(level*indent + '{ None }')
  

def df_to_hiercolor(df):
  # Initialize: 
  # 1) create new first column called 'root'
  # 2) convert last column (lowest layer) to nodes
  df.insert(loc=0, column='root', value=np.full(len(df), 'root'))
  print(df)
  #df.insert(loc=0, column='root', value=np.zeros(len(df)))
  def init_last_col(row):
    return json.dumps(None if row[-1]=='?' \
                      else {
                        'value': row[-1],
                        'color': None,
                        'subnodes': 0,
                        'subsum': row[-1] if isinstance(row[-1], (int, float)) else 0,
                        'children': None
                      }
    )
  df[df.columns[-1]] = df.apply(init_last_col, axis=1).values

  def concat_last_cols_as_json(row):
    str_jsons = row.iloc[-1]
    converted_jsons = []
    subsum = 0
    subnodes = 0
    for str_json in str_jsons:
      dict_json = json.loads(str_json)
      converted_jsons += [dict_json]
      if dict_json:
        subsum += dict_json['subsum']
        subnodes += 1 + dict_json['subnodes'] # parent + children
      else:
        subnodes += 1
    return json.dumps(None if row[-2]=='?' \
                      else {
                        'value': row[-2],
                        'color': None,
                        'subnodes': subnodes, #number of subnodes
                        'subsum': subsum, #sum over values in subnodes (if numeric)
                        'children': converted_jsons
                      }
    )
  for i in range(df.shape[1]-1):
    all_except_last_col = df.columns.tolist()[:-1] 
    next_to_last_col = all_except_last_col[-1]
    last_col = df.columns.tolist()[-1]

    # Collapse last column within group defined in prev col
    df = df.groupby(all_except_last_col)[last_col] \
           .apply(list) \
           .reset_index() 
    df[next_to_last_col] = df.apply(concat_last_cols_as_json, axis=1)
    df.drop(last_col, inplace=True, axis=1)
  return json.loads(df.iloc[0, 0])

def hier_circle_color(hier, x=0, y=0, th=0, r=90):
  if hier:
    children = hier['children']

    # Plot current point
    hier['color'] = [x, y]
    
    if children:
      num_children = len(children)
      # repeat for every child
      ## define angles 
      delta = 2*pi/num_children

      def is_odd(number):
        return (number % 2) != 0

      if is_odd(num_children):
        angle_shift = 0.0
      else:
        angle_shift = delta/2.0

      ## define new radius (loc: law of cosines)
      loc_angle = 2*pi/(3*num_children)
      child_r_squared = 2*(r**2)*(1 - np.cos(loc_angle))
      child_r = np.sqrt(child_r_squared)
      child_r = 0.80*child_r # Shrink radius by a factor (tunable)

      for i, child in enumerate(children):
        child_th = th + i*delta + angle_shift
        child_x = r*np.cos(child_th)
        child_y = r*np.sin(child_th)
        hier_circle_color(
          hier=child,
          x   = x + child_x,
          y   = y + child_y,
          th  = child_th,
          r   = child_r
        )

def hiercolor_to_table(hier, color_table=False):
  """convert hierarchy to a table format
     recursive!
  """
  if color_table:
    value = hier['color']
  else:
    value = hier['value']

  children = hier['children']

  if children:
    subtables = []
    subtable_widths = []
    for i, child in enumerate(children):
      if child: # i.e. not a null entry
        subtable = hiercolor_to_table(child, color_table)
        subtable_widths += [len(subtable[0])]
        subtables += [subtable]
      else:
        subtable = [[None]]
        subtable_widths += [1]
        subtables += [subtable]
    max_subtable_width = max(subtable_widths)    
    
    table = []
    for subtable, subtable_width in zip(subtables, subtable_widths):
      left_fill = (max_subtable_width - subtable_width)*[None]
      for row in subtable:
        table_row = [[value] + row + left_fill]
        table += table_row
  else:
    table = [[value]]

  return table

def table_color_maps(hier, keep_root=False, color_of_missing=[0, 0], L=50, L_alternating=None):
  if L < 0 or 100 < L:
    print('Input Error in table_color_maps()!')
    print('L has to be a value between 0 and 100')
  if L_alternating:
    if L_alternating < 0 or 100 < L_alternating:
      print('Input Error in table_color_maps()!')
      print('L_alternating has to be a value between 0 and 100')

  color_table = hiercolor_to_table(hier, color_table=True)
  nrows = len(color_table)
  ncols = len(color_table[0])

  color_of_missing = [L] + color_of_missing
  if not L_alternating:
    L_alternating = L

  row_colors = []
  for r in range(nrows):
    even = (r % 2 == 0)
    if even:
      L_row = L
    else: # odd
      L_row = L_alternating

    if color_table[r][-1]:
      row_color = [L_row] + color_table[r][-1]
    for c in range(ncols):
      if color_table[r][c] == None:
        color_table[r][c] = color_of_missing
        if color_table[r][c-1] != color_of_missing:
          row_color = color_table[r][c-1]
      else:
        color_table[r][c] = [L_row] + color_table[r][c]
    row_colors += [row_color]

  if keep_root:
    return color_table, row_colors
  else:
    for r in range(nrows):
      del color_table[r][0]
    return color_table, row_colors

def luv_to_rgb(luv_colors):
  if len(np.shape(luv_colors)) == 2:
    return luv2rgb(np.array([luv_colors]))[0]
  elif len(np.shape(luv_colors)) == 3:
    return luv2rgb(np.array(luv_colors))

def print_table(table):
  for row in table:
    print(row)

def print_color_table(table):
  for row in table:
    formatted_row = [ '({:0.2f}, {:1.2f}, {:2.2f})'.format(L, x, y) for L, x, y in row]
    print(formatted_row)


def hier_to_sunburst_data():
  """
     Prepare HierColor for dash-sunburst diagram
  """
  pass



def table_hiercolor(df, keep_root=False, color_of_missing=[0, 0], 
                    L=50, L_alternating=None):
  df.fillna('?', inplace=True)
  hier = df_to_hiercolor(df)
  hier_circle_color(hier)
  color_table, row_colors = \
    table_color_maps(hier, 
                     keep_root = keep_root, 
                     color_of_missing = color_of_missing,
                     L = L,
                     L_alternating = L_alternating)
  return luv_to_rgb(color_table), luv_to_rgb(row_colors)




if __name__ == '__main__':

  text_input_1= """
  a,b,c,d,e,f,g,h
  1,2,3,4,5,6,7,1
  1,2,3,4,5,6,7,
  1,2,,4,5,6,7,
  1,2,3,4,5,6,7,4
  2,2,3,4,,,,
  2,2,3,4,5,7,8,2
  3,2,3,4,5,3,,
  3,2,3,4,5,7,9,2
  4,2,3,4,5,,,
  4,2,3,4,5,,,
  4,2,3,4,5,,,
  """
  
  text_input_2= """
  a,b
  1,1
  1,2
  2,1
  2,2
  3,1
  3,2
  3,3
  3,4
  """
  
  text_input_3= """
  a,b,c
  1,,1
  1,,1
  2,1,1
  2,2,2
  3,1,1
  3,2,3
  3,2,6
  3,2,6
  """
  
  df = pd.read_csv(StringIO(text_input_3), delimiter=',')
  
  print('Table Color Mappings')
  color_table, row_colors = table_hiercolor(df, L=50, L_alternating=51)
  print('Color Table')
  print_color_table(color_table)
  print('Row Colors')
  for col in row_colors:
    print(col)
  print()

  #df = pd.read_csv('data/titanic.txt')
  #df['Age'] = df['Age'].apply(pd.to_numeric, errors = 'coerce')
  #def age_groups(age):
  #  if   -1 < age and age < 17: return 'child'
  #  elif 16 < age and age < 26: return 'youth'
  #  elif 25 < age and age < 61: return 'adult'
  #  elif 60 < age: return 'old'
  #  else: return '?'
  #df['AgeRange'] = df['Age'].apply(age_groups)
  #df.drop(['Age'], axis=1, inplace=True)
  #df = df.groupby(['Sex', 'AgeRange', 'Pclass', 'Survived']) \
  #          .size() \
  #          .reset_index(name='Count')
  #print(df.head(5))
  #
  #print('Table Color Mappings')
  #color_table, row_colors = table_hiercolor(df, L=50, L_alternating=51)
  #print('Color Table')
  #print_color_table(color_table)
  #print('Row Colors')
  #for col in row_colors:
  #  print(col)
  #print()


