#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

import json
# dumps: obj -> str
# loads: str -> obj
#
#d = {'a': 1,  'b':[2,2,1]}
#print(d, type(d))
#d = json.dumps(d)
#print(d, type(d))
#d = json.loads(d)
#print(d, type(d))
def print_json(input_json):
  # If str-json, convertto dict
  # See: https://stackoverflow.com/questions/26745519/converting-dictionary-to-json-in-python
  if isinstance(input_json, str):
    input_json = json.loads(input_json)

  print(json.dumps(input_json,
                   indent=2,
                   sort_keys=True))


def df_to_json(df):
  df.insert(loc=0, column='root', value=np.zeros(len(df)))
  for i in range(df.shape[1]-1):
    all_except_last_col = df.columns.tolist()[:-1] 
    next_to_last_col = all_except_last_col[-1]
    last_col = df.columns.tolist()[-1]

    # Collapse last column within group defined in prev col
    df = df.groupby(all_except_last_col)[last_col] \
           .apply(list) \
           .reset_index() 
    def concat_last_cols_as_json(row):
      first_list_element = row.iloc[-1][0]
      alphanumeric = str(first_list_element).replace('.', '', 1).isalnum() \
        or str(first_list_element) == '?'
      if alphanumeric:
          return json.dumps({row.iloc[-2]: row.iloc[-1]})
      else: # unpack sub jsons 
        str_jsons = row.iloc[-1]
        converted_jsons = []
        for str_json in str_jsons:
          converted_jsons += [json.loads(str_json)]
        return json.dumps({row.iloc[-2]: converted_jsons})
    df[next_to_last_col] = df.apply(concat_last_cols_as_json, axis=1)
    df.drop(last_col, inplace=True, axis=1)

  print_json(json.loads(df.iloc[0].values[0]))

def init_last_col(row):
    return json.dumps(None if row[-1]=='?' \
                      else {
                        #'row_index': row.name, 
                        #'col_index': len(row)-2, # additional (-1) because of root col
                        'value': row[-1],
                        'color': None,
                        'subnodes':0, #number of subnodes
                        'subsum': row[-1] if isinstance(row[-1], (int, float)) else 0,
                        'children': None
                      })
  
def df_to_json_v2(df):
  # Todo
  # * insert empty lists at end or None
  # * replace '?'/missing with empty lists
  # * return 'value', cell=(row, col), (bottom indicator not 
  #   needed as it is as it is identified by empty list 
  #   (I at least think this will do). Will be used to 
  #    create row-mapping for "entire row coloring")
  # NOTE: the hierarchy nodes can have only 1 missing type child,
  #       (another missing would be included in group).
  # Endpoint? - If any instance of None (in children) then endpoint, 
  #             and hence row-color defining
  #             * should i have a field for this??
  # NOTE - ERROR: finding cell position is ruined when
  #               it is set while collapsing dataframe!!!!!!!!!!!!!!!!

  # Initialize
  ## insert root node
  df.insert(loc=0, column='root', value=np.zeros(len(df)))
  ## create nodes of last row
  df[df.columns[-1]] = df.apply(init_last_col, axis=1).values

  for i in range(df.shape[1]-1):
    all_except_last_col = df.columns.tolist()[:-1] 
    next_to_last_col = all_except_last_col[-1]
    last_col = df.columns.tolist()[-1]

    # Collapse last column within group defined in prev col
    df = df.groupby(all_except_last_col)[last_col] \
           .apply(list) \
           .reset_index() 
    def concat_last_cols_as_json(row):
      str_jsons = row.iloc[-1]
      converted_jsons = []
      subsum = 0
      subnodes = 0
      for str_json in str_jsons:
        dict_json = json.loads(str_json)
        converted_jsons += [dict_json]
        subsum += dict_json['value']
        subnodes += 1 + dict_json['subnodes'] # parent + children
      return json.dumps(None if row[-2]=='?' \
                        else {
                          #'row_index': row.name, 
                          #'col_index': len(row)-3, # additional (-1) because of root col
                          'value': row[-2],
                          'color': None,
                          'subnodes': subnodes, #number of subnodes
                          'subsum': subsum, #sum over values in subnodes (if numeric)
                          'children': converted_jsons
                        })

    df[next_to_last_col] = df.apply(concat_last_cols_as_json, axis=1)
    df.drop(last_col, inplace=True, axis=1)
  #print_json(json.loads(df.iloc[0].values[0]))
  return json.loads(df.iloc[0, 0])

# Pandas data frame to dictioairy:
# https://stackoverflow.com/questions/24374062/pandas-groupby-to-nested-json/24376671
# Didn't understand this one! Read it again and see if they've found a better solution  !!!


def json_to_table(hier, color_table=False):
  """convert hierarchy to a table format"""
  if color_table:
    value = hier['color']
  else:
    value = hier['value']

  children = hier['children']

  if children:
    subtables = []
    subtable_widths = []
    for i, child in enumerate(children):
      subtable = json_to_table(child, color_table)
      subtable_widths += [len(subtable[0])]
      subtables += [subtable]
    max_subtable_width = max(subtable_widths)    
    
    table = []
    for subtable, subtable_width in zip(subtables, subtable_widths):
      left_fill = (max_subtable_width - subtable_width)*['?']
      for row in subtable:
        table_row = [[value] + row + left_fill]
        table += table_row
  else:
    table = [[value]]
  return table

def print_table(table):
  for row in table:
    print(row)


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
  
  df = pd.read_csv(StringIO(text_input_2), delimiter=',')
  df.fillna('?', inplace=True)
  #df.fillna(None, inplace=True)
  
  print(df)
  hier = df_to_json_v2(df)
  print_json(hier)
  print(type(hier))
  print()
  table = json_to_table(hier, color_table=False)
  color_table = json_to_table(hier, color_table=True)
  
  print('Table')
  print_table(table)
  print()

  print('Color Table')
  print_table(color_table)

  print()
