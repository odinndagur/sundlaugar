import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

with open('pools.json','r') as f:
    data = json.load(f)

for x in data:
    x['address'] = x['address'].strip()
    if(len(x['coordinates']) > 0):
        x['longitude'], x['latitude'] = float(x['coordinates'].split(',')[0]), float('-' + x['coordinates'].split(',')[1])
    # print(x)
# print(data)
df = pd.DataFrame(data=data)

BBox = (df.longitude.min(),   df.longitude.max(),      
         df.latitude.min(), df.latitude.max())
print(df)