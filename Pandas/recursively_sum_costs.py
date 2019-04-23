#!/usr/bin/env python3

import pandas as pd

bom = pd.DataFrame(
    {
        'ID': [0,1,2,3,4],
        'parent_ID': [-1, 0, 0, 1, 2],
        'cost': [0.00, 0.00, 0.00, 0.50, 1.66],
    }
)
reversed_IDs = (id for id in reversed(bom.ID))
print(bom)
while 1:
    try:
        print('-------------------------------')
        current_id = next(reversed_IDs)
        current_parent = bom.loc[current_id].parent_ID
        bom.loc[current_parent, "cost"] += bom.loc[current_id, "cost"]
        print(bom)
        print('-------------------------------')
    except KeyError:
        print('KeyError reached because none of the rows in the DataFrame have an index of -1')
        break
