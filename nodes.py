"""
Nodes are derived from Navstreet Zlevel file
Steps: Zlevel file > Drop nodeids with 0 > Combined 5 files into 1 node file for entire CA
Population density extracted using ArcGIS is formated
"""
import os
import pandas as pd
import geopandas as gpd

if not os.path.isfile('../data/midstages/zlevel_combined.csv'):
    print('====== Started combining ZLevel files ======')
    commonpath = '../from_Here/original_HERE'
    filenames = ['here_map_11/here_map_11_shapefiles/Zlevels.shp', 'here_map_12-20191207T191053Z-001/here_map_12/here_map_12_shapefiles/Zlevels.shp',
    'here_map_13/here_map_13_shapefiles/Zlevels.shp','here_map_14/here_map_14_shapefiles/Zlevels.shp','here_map_15-20191207T193135Z-001/here_map_15/here_map_15_shapefiles/Zlevels.shp' ]

    print("=== Loading the Zlevel geodataframes =====")
    fullpath = [os.path.join(commonpath, f) for f in filenames]
    zlevel_combined = pd.concat(map(gpd.read_file, fullpath))
    zlevel_combined.to_csv('../data/midstages/zlevel_combined.csv',index = False)
    print("=== Completed writing =====")

print('====== Zlevel Combined already exists. Started  creating Nodes file ======')
zlevel_combined = pd.read_csv('../data/midstages/zlevel_combined.csv') 
print("Length of zlevel file", len(zlevel_combined))
nodes = zlevel_combined[zlevel_combined.NODE_ID!=0] #For Nodes files from z level(dropping 0 node ids)
print("Number of nodes", len(nodes))
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

# adding the required attributes
new = nodes['geometry'].str.split(expand=True)
nodes['LON']= new[1].str[1:]
nodes['LAT']= new[2].str[:-1]
nodes['geom'] = nodes['geometry'] #reductant column, making it to be consistent with the previous format accepted by Mobiliti

#Write to csv and shapefile
req_columns = ['NODE_ID', 'geometry','LON','LAT',"geom"]
nodes[req_columns].to_csv('../data/july2021/all_nodes.csv', index = False)

# # Calculating Population density for nodes - File extracted using ArcGIS
# nodes_pop = pd.read_csv('../data/midtages/nodes_pop_density.csv')
# nodes_pop.rename(columns = {'RASTERVALU': 'pop_density'}, inplace = True)
# nodes_pop = nodes_pop.drop(['OBJECTID'], axis = 1)
# nodes_pop.to_csv('../data/midstages/nodes_pop_density.csv', index = False) # replace the file
