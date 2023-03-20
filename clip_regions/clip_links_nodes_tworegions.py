"""
Generate networks for two regions combined. 
Eg - SACOG and San Diego together. 
"""

import yaml
import pandas as pd
import geopandas as gpd
import os
import filter_clipregions as fcr

config_file = "config.yaml"
a_yaml_file = open(config_file)
config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

alllinks_path =  config["clip"]["alllinks_processed"]
alllinksgeom_path =  config["clip"]["alllinks_processed_geom"]
allnodes_path = config["clip"]["allnodes_processed"]
linksname = config["write"]["links_filename"]
nodesname = config["write"]["nodes_filename"]

boundary_path_one = config["clip"]["boundary"]
boundary_path_two = config["clip"]["boundary_two"]
cityname_one = config["write"]["cityname"]
cityname_two = config["write"]["cityname_two"]
cityname = cityname_one + '_' + cityname_two
savepath_final = '../../data/' + cityname + '/final'
savepath_mid = '../../data/' + cityname + '/midstage'


if not os.path.isfile(alllinksgeom_path):
    print("Creating geom for all CA links")
    alllinks = pd.read_csv(alllinks_path) # latest links edited
    allnodes = pd.read_csv(allnodes_path)
    alllinksgeom = fcr.links_geom(alllinks, allnodes)
    alllinksgeom_gdf = fcr.geom_shp(alllinksgeom, savepath = "../../data/july2021")           


print("====== Creating the rectangular buffer boundary from the TAZ shapefile ========")
clipboundary = fcr.process_two_boundary(boundary_path_one, boundary_path_two) #rectangular buffer boundary combined

print("====== Clipping links to the the boundary ========")
alllinksgeom_gdf = gpd.read_file(alllinksgeom_path)
links_clipped = fcr.clip_links(alllinksgeom_gdf,clipboundary)
if not os.path.exists(savepath_mid):
    os.makedirs(savepath_mid)
links_clipped.to_csv(os.path.join(savepath_mid, "preprocess_clippedlinks.csv"), index = False)

print("====== Clipping nodes based on clipped links file ========")
allnodes = pd.read_csv(allnodes_path)
sac_refnodes = links_clipped['REF_IN_ID'].to_list()
sac_nrefnodes = links_clipped['NREF_IN_ID'].to_list()
sacnodes = sac_refnodes+ sac_nrefnodes
sacnodes_unique = set(sacnodes)
nodes_clipped = allnodes[allnodes['NODE_ID'].isin(sacnodes_unique)]
nodes_clipped.to_csv(os.path.join(savepath_mid, "preprocess_clippednodes.csv"), index = False)

print("==== Applying the strongly connected network filter =====")
nodes_path = os.path.join(savepath_mid, "preprocess_clippednodes.csv")
links_path = os.path.join(savepath_mid, "preprocess_clippedlinks.csv")
links_connected, nodes_connected = fcr.full_connected_filter(nodes_path, links_path)

#rename links attributes name which gets truncated in the geopandas clip step
rename_cols = {'NUM_PHYS_L': 'NUM_PHYS_LANES', 'LENGTH(met': 'LENGTH(meters)',
 'CAPACITY(v':'CAPACITY(veh/hour)'}
links_connected.rename(columns = rename_cols , inplace = True)
cols_interest = ['LINK_ID', 'ST_NAME', 'REF_IN_ID', 'NREF_IN_ID', 'FUNC_CLASS',
       'DIR_TRAVEL', 'NUM_PHYS_LANES', 'SPEED_KPH', 'LENGTH(meters)',
       'CAPACITY(veh/hour)', 'RAMP']
links_connected = links_connected[cols_interest]

if not os.path.exists(savepath_final):
    os.makedirs(savepath_final)
final_list = [[links_connected, linksname], [nodes_connected, nodesname]]
for f in final_list:
    fcr.write_file(f[0], savepath= savepath_final, savename = cityname + '_' + f[1] )
print("======== Finished writing the clipped links and nodes files ======") 


