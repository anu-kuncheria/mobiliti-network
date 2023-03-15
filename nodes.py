import pandas as pd
import numpy as np
import os
import geopandas as gpd

"""
Nodes are derived from Navstreet Zlevel file
Steps: Zlevel file > Drop nodeids with 0 > Combined 5 files into 1 node file for entire CA
Population density extracted using ArcGIS is formated
"""

zlevelpath = '../from_Here/original_HERE'
filenames = ['here_map_11/here_map_11_shapefiles/Zlevels.shp', 'here_map_12-20191207T191053Z-001/here_map_12/here_map_12_shapefiles/Zlevels.shp',
'here_map_13/here_map_13_shapefiles/Zlevels.shp','here_map_14/here_map_14_shapefiles/Zlevels.shp','here_map_15-20191207T193135Z-001/here_map_15/here_map_15_shapefiles/Zlevels.shp' ]

print("=== Loading the Zlevel geodataframes =====")
zleveldfs = []
for file in filenames:
    zleveldfs = [gpd.read_file(os.path.join(zlevelpath, file))]
print("--- Number of dataframes are ---", len(zleveldfs))
print("Length of first df", len(zleveldfs[0]))
zlevel_combined = pd.concat([zleveldfs[i] for i in range(len(zleveldfs))])
zlevel_combined.to_csv('../midstages/zlevel_combined.csv',index = False)
print("=== Completed writing =====")

#For Nodes files from z level(dropping 0 node ids)
nodes = zlevel_combined[zlevel_combined.NODE_ID!=0] #6.5Million nodes
print("Nodes number", len(nodes))
#changing the order of columns  #6.5Million nodes
cols = nodes.columns.tolist()
cols = cols[2:7] + [cols[1]] + [cols[7]] + [cols[0]]
nodes = nodes[cols]
#To get unique node ids
nodes.drop(columns = ['LINK_ID'],inplace = True)
nodes = nodes.drop_duplicates(subset='NODE_ID', keep="first")
nodes = nodes.reset_index(drop = True)
print(nodes['Z_LEVEL'].value_counts())

#Sanity check
print(len(nodes.drop_duplicates(subset='geometry', keep="first"))) # length ofnode ids that are duplicated in geometry. This shows that some intersections with same geometry having differnt z levels are given differnt node ids.

#Write to csv and shapefile
nodes.to_csv('../midtages/nodes_all.csv', index = False)
nodes.to_file(driver='ESRI Shapefile', filename='nodes_all.shp')

# Calculating Population density for nodes - File extracted using ArcGIS
nodes_pop = pd.read_csv('../midtages/allnodes_popden.csv')
nodes_pop.rename(columns = {'RASTERVALU': 'pop_density'}, inplace = True)
nodes_pop = nodes_pop.drop(['OBJECTID'], axis = 1)
nodes_pop.to_csv('../final/allnodes_population_density.csv', index = False)
