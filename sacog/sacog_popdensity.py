import pandas as pd
import numpy as np

# Pop density extracted from GHS dataset for nodes in ArcGIS
popdensity_pre = pd.read_csv('../../sacog_region_data/mid_processing/popdensity_sacog_preprocess.csv')
print(len(popdensity_pre))
print(popdensity_pre.columns)

popdensity = popdensity_pre[['NODE_ID', 'RASTERVALU']]
popdensity.rename(columns = {'RASTERVALU':'popdensity'}, inplace = True)
print('*****', len(popdensity[popdensity['popdensity']<0]))
popdensity['popdensity'] = popdensity['popdensity'].replace([-9999.], 0)
print('***', len(popdensity[popdensity['popdensity']<0]))
print(popdensity.isnull().sum())
print(len(popdensity))
popdensity.to_csv('../../sacog_region_data/final/sacog_popdensity.csv', index = False)




