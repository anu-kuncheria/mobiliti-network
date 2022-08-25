import pandas as pd
import numpy as np

# Pop density extracted from GHS dataset for nodes in ArcGIS
popdensity_pre = pd.read_csv('../../sacog_region_data/mid_processing/popdensity_sacog_preprocess.csv')
print(len(popdensity_pre))
print(popdensity_pre.columns)

popdensity = popdensity_pre[['NODE_ID', 'RASTERVALU']]
popdensity.rename(columns = {'RASTERVALU':'pop_density'}, inplace = True)
print(popdensity.isnull().sum())
print(len(popdensity))
popdensity.to_csv('../../sacog_region_data/final/sacog_popdensity.csv', index = False)




