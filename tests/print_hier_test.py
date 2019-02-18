hierJ = {'loc': '0',
         'rowid': None,
         'color_xy': (0.0,0.0),
         'subnodes': None,
         'children': [
             {'loc': '0_1',
              'rowid': None,
              'color_xy': (0.0,0.0),
              'subnodes': None,
              'children': [    
                  {'loc': '0_1_1',
                   'rowid': None,
                   'color_xy': (0.0,0.0),
                   'subnodes': None,
                   'children': []},
                  {'loc': '0_1_2',
                   'rowid': None,
                   'color_xy': (0.0,0.0),
                   'subnodes': None,
                   'children': []},
                  {'loc': '0_1_3',
                   'rowid': None,
                   'color_xy': (0.0,0.0),
                   'subnodes': None,
                   'children': [  
                       {'loc': '0_1_3_1',
                        'rowid': None,
                        'color_xy': (0.0,0.0),
                        'subnodes': None,
                        'children': []},
                       {'loc': '0_1_3_2',
                        'rowid': None,
                        'color_xy': (0.0,0.0),
                        'subnodes': None,
                        'children': [
                            {'loc': '0_1_3_2_1',
                             'rowid': None,
                             'color_xy': (0.0,0.0),
                             'subnodes': None,
                             'children': [
                                 {'loc': '0_1_3_2_1_1',
                                  'rowid': None,
                                  'color_xy': (0.0,0.0),
                                  'subnodes': None,
                                  'children': []},
                                 {'loc': '0_1_3_2_1_2',
                                  'rowid': None,
                                  'color_xy': (0.0,0.0),
                                  'subnodes': None,
                                  'children': []}
                            ]}
                       ]}, 
                       {'loc': '0_1_3_3',
                        'rowid': None,
                        'color_xy': (0.0,0.0),
                        'subnodes': None,
                        'children': []}
                  ]},
                  {'loc': '0_1_4',
                   'rowid': None,
                   'color_xy': (0.0,0.0),
                   'subnodes': None,
                   'children': []}
             ]},
             {'loc': '0_2',
              'rowid': None,
              'color_xy': (0.0,0.0),
              'subnodes': None,
              'children': []},
             {'loc': '0_3',
              'rowid': None,
              'color_xy': (0.0,0.0),
              'subnodes': None,
              'children': []}
]}

     
def print_json_hier(hier=None, level=0):
  if not hier:
    print("Error print_hier(hier):: no input hierarchy given!")
    return
  
  children = hier['children']
  indent = 4*level*' '
  line = indent
  for i, (key, val) in enumerate(hier.items()):
    if i == 0:
      line += '{'
    else:
      line += ' '

    if key == 'children' and val:
      line += str(key)+' : ['
      print(line)
      for child in hier['children']:
        print_json_hier(child, level=level+1)
      print(indent+']}')
    elif key == 'children' and not val:
      line += str(key)+' : []}'
      print(line)
    else:
      line += str(key)+' : '+str(val)+','
      print(line)
    line = indent

print_json_hier(hierJ)
