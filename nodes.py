import pandas as pd
import numpy as np
import os
from geopandas import GeoDataFrame

# Nodes derived from Navstreet Zlevel
# Pipeline: Zlevel file > Drop nodeids with 0 > Combined 5 files into 1 node file for entire CA
zlevel1 = gpd.read_file('..\here_map_11\here_map_11_shapefiles\Zlevels.shp')
zlevel2 = gpd.read_file('..\here_map_12\here_map_12_shapefiles\Zlevels.shp')
zlevel3 = gpd.read_file('..\here_map_13\here_map_13_shapefiles\Zlevels.shp')
zlevel4 = gpd.read_file('..\here_map_14\here_map_14_shapefiles\Zlevels.shp')
zlevel5 = gpd.read_file('..\here_map_15\here_map_15_shapefiles\Zlevels.shp')
zlevel_combined = zlevel1.append(zlevel2, sort = False)
zlevel_combined = zlevel_combined.append(zlevel3, sort = False)
zlevel_combined = zlevel_combined.append(zlevel4, sort = False)
zlevel_combined = zlevel_combined.append(zlevel5, sort = False)
zlevel_combined.to_csv('zlevel_combined.csv',index = False)

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
nodes.to_csv('nodes_all.csv', index = False)
crs = epsg 4326
nodes.to_file(driver='ESRI Shapefile', filename='nodes_all.shp')

# Calculating Population density for nodes
nodes_pop = pd.read_csv('allnodes_popden.csv')
nodes_pop.rename(columns = {'RASTERVALU': 'pop_density'}, inplace = True)
nodes_pop = nodes_pop.drop(['OBJECTID'], axis = 1)
nodes_pop.to_csv('allnodes_pop.csv', index = False)
